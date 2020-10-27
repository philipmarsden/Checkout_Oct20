import configparser
import psycopg2 #postgresql db adapter
from locs import CONFIG_PATH
from create_views_sql import create_views_queries


def create_views (cur, conn):
    """run each of the view creation queries from the create_views_sql program"""
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    """Connect to the database with details in config file, create the views over the schema to
    answer the specific business questions
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['STAGE'].values()))
    cur = conn.cursor()
    
    #create the views
    create_views(cur, conn)
    
    conn.close()
    
    
if __name__ == "__main__":
    main()
    