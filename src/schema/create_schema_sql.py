
#DROP TABLES
time_dim_drop = "drop table if exists time_dim"
url_dim_drop = "drop table if exists url_dim"
postcode_dim_drop = "drop table if exists postcode_dim"
user_dim_drop = "drop table if exists user_dim"
pageviews_fact_drop = "drop table if exists pageviews_fact"
pageviews_fact_stg_drop = "drop table if exists pageview_stg"


# CREATE TABLES
time_dim_create = ("""
create table time_dim (
    time_sk bigint IDENTITY (1,1) PRIMARY KEY
    ,time_stamp timestamp UNIQUE NOT NULL
    ,year integer NOT NULL
    ,month integer NOT NULL
    ,week integer NOT NULL
    ,day integer NOT NULL
    ,hour integer NOT NULL
    )
""")

url_dim_create = ("""
create table url_dim (
    url_sk bigint IDENTITY (1,1) PRIMARY KEY
    ,url_full VARCHAR(255) UNIQUE NOT NULL
    
    )
""")

postcode_dim_create = ("""
create table postcode_dim (
    postcode_sk bigint IDENTITY (0,1) PRIMARY KEY
    ,short_postcode VARCHAR(4) UNIQUE NOT NULL
    )
""")

user_dim_create = ("""
create table user_dim (
    user_sk bigint IDENTITY (1,1) PRIMARY KEY
    ,user_id bigint UNIQUE NOT NULL
    ,current_postcode VARCHAR(4)
    )
""")

page_views_fact_create= ("""
create table pageviews_fact (
    time_sk bigint NOT NULL
    ,url_sk bigint NOT NULL
    ,user_sk bigint NOT NULL
    ,postcode_sk bigint NOT NULL
    ,page_views bigint
    ,primary key (time_sk, url_sk ,user_sk ,postcode_sk)
    )
    PARTITION BY LIST (time_sk)
""")


    
#create staging table - join and summariese once rather than in each query
pageview_fact_stg_create = ("""
create table pageview_stg (
    time_stamp timestamp 
    ,time_sk bigint
    ,url varchar(255)
    ,url_sk bigint
    ,user bigint
    ,user_sk bigint
    ,postcode varchar(4)
    ,postcode_sk bigint
    ,pageviews bigint
    )
""")

postcode_default_insert = ("""
insert into postcode_dim (postcode_sk, short_postcode)
values (null, 'XX99')
""")

create_table_queries = ['time_dim_create', 'url_dim_create', 'postcode_dim_create', 'user_dim_create', 'page_views_fact_create', 'pageview_fact_stg_create']
drop_table_queries = ['time_dim_drop', 'url_dim_drop', 'postcode_dim_drop', 'user_dim_drop', 'page_views_fact_drop']
default_values_queries = ['postcode_default_insert']


