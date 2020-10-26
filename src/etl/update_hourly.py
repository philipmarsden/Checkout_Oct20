import configparser
from locs import CONFIG_PATH
import psycopg2
from update_sql import insert_dims_queries_hourly, insert_stg_queries_hourly, insert_fact_queries_hourly


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
        
        
def main():
    """Connect to the database with details in config file, extact data from staging
    tables and insert data into the database.
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH + '\\dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['STAGE'].values()))
    cur = conn.cursor()
    
    
    #update dimensions
    update_dimensions(cur, conn)
    
    #insert into staging table
    update_stg_tables(cur, conn)
    
    #insert fact data
    update_fact_tables(cur, conn)
  
    conn.close()
	
    
    
if __name__ == "__main__":
    main()	