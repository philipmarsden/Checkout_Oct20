import configparser
from locs import CONFIG_PATH
import psycopg2
import datetime as dt
from update_sql import insert_queries_daily, update_queries_daily
from job_table_queries import * as jq

def insert_new(cur, conn):
    """run each of the insert queries from the update_sql program - only the daily ones"""
    for query in insert_queries_daily:
        cur.execute(query)
        conn.commit()
        
def update_new(cur, conn):
    """run each of the update queries from the update_sql program - daily updates"""
    for query in update_queries_daily:
        cur.execute(query)
        conn.commit()


def main():
    """Connect to the database with details in config file, extact data from staging
    tables and insert data into the database.
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH + '\\dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['STAGE'].values()))
    cur = conn.cursor()
    
    starttime = dt.datetime.now()
    
    #get expected load size
    cur.execute(jq.get_expected_rows_daily)
    daily_exp_rows = cur.fetchone()[0]
    
    # build straight from the first staging table
    # insert new users & postcodes
    insert_new(cur, conn)
    
    # update all postcodes
    #update users / postcodes in fact table where default values exist with now most recent location
    update_new(cur, conn)
    
    #get new table size
    cur.execute(jq.get_imported_rows_daily)
    daily_act_rows = cur.fetchone()[0]
    
    #get the number of null values
    cur.execute(jq.get_null_values_daily)
    #need to check what will come out here because im not 100% sure but assume its a list of values, we add them all up
    column_nulls = cur.fetchone()[0]
    daily_nulls = sum(column_nulls)
    
    #get end time
    endtime = dt.datetime.now()
    
    #update the job table
    jobstats_sql = jq.job_data_sql(starttime, endtime, 'dly', daily_exp_rows, daily_act_rows, daily_nulls, 'Y')
    cur.execute(jobstats_sql)
    conn.commit()
    
    conn.close()
    
    
if __name__ == "__main__":
    main()