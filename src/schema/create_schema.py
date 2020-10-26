import configparser
import psycopg2 #postgresql db adapter
from locs import CONFIG_PATH
from create_schema_sql import create_table_queries, drop_table_queries, default_values_queries


def drop_tables (cur, conn):
    """run each of the drop table queries from the create_schema_sql program"""
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
       

def create_tables(cur, conn):
    """run each of the create table queries from the create_schema_sql program"""
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
        
def default_missing_values(cur, conn):
    """run the queries to add the first sk aligned to missing values into the tables"""
    for query in default_values_queries:
        cur.execute(query)
        conn.commit()
       
        
def main():
    """Connect to the database with details in config file, drop existing tables in db and
    recreate the schema
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['STAGE'].values()))
    cur = conn.cursor()
    
    #remove the existing tables
    drop_tables(cur, conn)
    
    #replace the tables with new ones
    create_tables(cur, conn)
    
    #add missing postcode value into table
    default_missing_values(cur, conn)
    
    conn.close()
    
    
if __name__ == "__main__":
    main()
    
    
    