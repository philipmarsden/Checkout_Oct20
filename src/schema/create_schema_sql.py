
#DROP TABLES
time_dim_drop = "drop table if exists time_dim"
url_dim_drop = "drop table if exists url_dim"
postcode_dim_drop = "drop table if exists postcode_dim"
user_dim_drop = "drop table if exists user_dim"
page_views_fact_drop = "drop table if exists page_views_fact"

# CREATE TABLES
time_dim_create = ("""
create table time_dim (
    time_sk bigint IDENTITY (1,1) PRIMARY KEY
    ,time_stamp timestamp NOT NULL
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
    ,url_full VARCHAR(255) NOT NULL
    
    )
""")

postcode_dim_create = ("""
create table postcode_dim (
    postcode_sk bigint IDENTITY (1,1) PRIMARY KEY
    ,short_postcode VARCHAR(4) NOT NULL DEFAULT
    )
""")

user_dim_create = ("""
create table user_dim (
    user_sk bigint IDENTITY (1,1) PRIMARY KEY
    ,user_id bigint NOT NULL
    ,current_postcode VARCHAR(4)
    )
""")

page_views_fact_create= ("""
    create table page_views_fact (
    time_sk bigint NOT NULL
    ,url_sk bigint NOT NULL
    ,user_sk bigint NOT NULL
    ,postcode_sk bigint NOT NULL
    ,page_views bigint
    ,primary key (time_sk, url_sk ,user_sk ,postcode_sk)
    )
""")

    
create_table_queries = ['time_dim_create', 'url_dim_create', 'postcode_dim_create', 'user_dim_create', 'page_views_fact_create']
drop_table_queries = ['time_dim_drop', 'url_dim_drop', 'postcode_dim_drop', 'user_dim_drop', 'page_views_fact_drop']



