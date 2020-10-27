# This probably only really needs to be run once and then populated so will just have it as a manual
# script that can be run to create. it doesn't need to be clever, and can be ajusted as needed.

import configparser
from locs import CONFIG_PATH
import psycopg2

create_job_table = ("""
create table job_tracker (
job_id IDENTITY (1,1) PRIMARY KEY
,starttime timestamp
,endtime timestamp
,job_type char(4)
,expected_rows bigint
,inserted_rows bigint
,null_values bigint
,completed char(1)
)
""")



def main():
    """Create a table to store job information
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH + '\\dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['STAGE'].values()))
    cur = conn.cursor()
    
    # create the job tracking table
    cur.execute(create_job_table)
    conn.commit()
    
    conn.close()
    
    
if __name__ == "__main__":
    main()