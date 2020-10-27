
get_expected_rows_daily = ("""
select count(*) from users_extract
""")

get_expected_rows_hourly = ("""
select count(*) from pageviews_extract
""")

get_inserted_rows_daily = ("""
select count(*) from user_dim
""")

#sum pageviews as this should match the total cols
get_inserted_rows_hourly = ("""
select sum(pageviews) from pageview_stg
""")

#count(<col>) will only count non-nulls so this can get the null count per column easily
get_null_values_daily = ("""
select 
    count(1) - count(user_id) as user_id_null
    ,count(1) = count(current_postcode) as pc_null
""")

get_null_values_hourly = ("""
select 
    count(1) - count(time_sk) as time_null
    ,count(1) - count(url_sk) as url_null
    ,count(1) - count(user_sk) as user_null
    ,count(1) - count(postcode_sk) as pc_null
""")


def job_data_sql (starttime, endtime, job_type, expected_rows, inserted_rows, null_values, completed):
    """create the sql query to load into the jobs table using data extracted throughout process"""
    
    sql_query = ("""
    insert into job_tracker (
        starttime
        ,endtime
        ,job_type
        ,expected_rows
        ,inserted_rows
        ,null_values
        ,completed
        )
    values 
        (
        null,?,?,?,?,?,?,?
        )
    """).format{starttime, endtime, job_type, expected_rows, inserted_rows, null_values, completed}
    
    return sql_query
    
   