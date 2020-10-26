import configparser
from locs import CONFIG_PATH
import psycopg2
from update_sql import insert_queries_daily, update_queries_daily

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
    
    # build straight from the first staging table
    # insert new users & postcodes
    insert_new(cur, conn)
    
    # update all postcodes
    #update users / postcodes in fact table where default values exist with now most recent location
    update_new(cur, conn)
    
    
    conn.close()
    
    
if __name__ == "__main__":
    main()