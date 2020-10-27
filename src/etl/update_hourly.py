import configparser
from locs import CONFIG_PATH
import psycopg2
import datetime as dt
from update_sql import insert_dims_queries_hourly, insert_stg_queries_hourly, insert_fact_queries_hourly, truncate_tables_queries
from job_table_queries import * as jq


def update_dimensions(cur, conn):
    """run each of the update queries from the update_sql program - hourly dimension updates"""
    for query in insert_dims_queries_hourly:
        cur.execute(query)
        conn.commit()
        
def update_stg_tables(cur, conn):
    """run each of the update queries from the update_sql program - hourly dimension updates"""
    for query in insert_stg_queries_hourly:
        cur.execute(query)
        conn.commit()

def update_fact_tables(cur, conn):
    """run each of the update fact table queries from the update_sql program - hourly updates"""
    for query in insert_fact_queries_hourly:
        cur.execute(query)
        conn.commit()
        
def truncate_tables (cur, conn):
    """run each of the truncate table queries from the update_sql program to remove existing data"""
    for query in truncate_tables_queries:
        cur.execute(query)
        conn.commit()   


      
def main():
    """Connect to the database with details in config file, extact data from staging
    tables and insert data into the database.
    """
    starttime = dt.datetime.now()
    
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH + '\\dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['STAGE'].values()))
    cur = conn.cursor()
    
    #get expected load size
    cur.execute(jq.get_expected_rows_hourly)
    hourly_exp_rows = cur.fetchone()[0]
    
    #update dimensions
    update_dimensions(cur, conn)
    
    #remove the data from the existing stg table
    truncate_tables(cur, conn)
    
    #insert into staging table
    update_stg_tables(cur, conn)
    
    #insert fact data
    update_fact_tables(cur, conn)
    
    #get new table size
    cur.execute(jq.get_imported_rows_hourly)
    hourly_act_rows = cur.fetchone()[0]
    
    #get the number of null values
    cur.execute(jq.get_null_values_hourly)
    #need to check what will come out here because im not 100% sure but assume its a list of values, we add them all up
    column_nulls = cur.fetchone()[0]
    hourly_nulls = sum(column_nulls)
    
    #get end time
    endtime = dt.datetime.now()
    
    #update the job table
    jobstats_sql = jq.job_data_sql(starttime, endtime, 'hrly', hourly_exp_rows, hourly_act_rows, hourly_nulls, 'Y')
    cur.execute(jobstats_sql)
    conn.commit()
  
    conn.close()
	
    
if __name__ == "__main__":
    main()	