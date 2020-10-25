import configparser
import psycopg2

def main():
    """Connect to the database with details in config file, extact data from staging
    tables and insert data into the database.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    
    conn.close()