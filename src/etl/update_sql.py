

#Insert Queries

# time dimension
tim_dim_insert = ("""
insert into time_dim (
    time_sk
    ,time_stamp
    ,year
    ,month
    ,week
    ,day
    ,hour
    )
    
select distinct
    null as time_sk
    ,dateadd(hour, datediff(hour, 0, pageview_datetime), 0) as time_stamp
    ,extract(year from pageview_datetime) as year
    ,extract(month from pageview_datetime) as month
    ,extract(week from pageview_datetime) as week
    ,extract(day from pageview_datetime) as day
    ,extract(hour from pageview_datetime) as hour
    
    from pageviews_extract
    
    ON CONFLICT (time_stamp) DO NOTHING
""")


# url dimension
url_dim_insert = ("""
insert into url_dim (
    url_sk
    ,url_full
    )
    
select distinct
    null as url_sk
    ,url as url_full
    
    from pageviews_extract
    
    ON CONFLICT (url_full) DO NOTHING
""")

#missing users
missing_users_insert = ("""
insert into users_dim (
    user_sk
    ,user_id
    
    )
    
select distinct
    null as user_sk
    ,user_id
    ,'XX99' as current_postcode
    
    from pageviews_extract
    
    where user_id not in (select distinct user_id from users_dim)
    
""")

#postcode dimension
postcode_dim_insert = ("""
insert into postcode_dim (
    postcode_sk
    ,short_postcode
    )
    
select distinct
    null as postcode_sk
    ,postcode as short_postcode
    
    from users_extract
    
    ON CONFLICT (short_postcode) DO NOTHING
""")

#user dimension
user_dim_insert = ("""
insert into user_dim (
    user_sk
    ,user_id
    ,current_postcode
    )
    
select 
    null as user_sk
    ,user as user_id
    ,postcode as current_postcode
    
    from users_extract 
    
    where user_id not in (Select distinct user_id from user_dim)
""")

user_dim_update = ("""
update user_dim 
    set ud.current_postcode = stg.postcode

    from user_dim ud, users_extract stg
    
    where ud.user_id = stg.user
""")


#Fact table staging
pageview_fact_stg_insert = ("""
insert into pageview_stg (
    time_stamp
    ,time_sk
    ,url
    ,url_sk 
    ,user
    ,user_sk
    ,postcode 
    ,postcode_sk
    ,pageviews
    )
    
select 
    pe.timestamp_h as time_stamp
    ,tm.time_sk
    ,pe.url
    ,u.url_sk
    ,pe.user
    ,us.user_sk
    ,us.short_postcode as postcode
    ,pc.postcode_sk
    ,pe.pageviews
    
    from (select 
            dateadd(hour, datediff(hour, 0, pe.pageview_datetime), 0) as timestamp_h
            ,url
            ,user
            ,count(*) as pageviews 
            
            from pageviews_extract
            
            group by timestamp_h, url, user
            
        ) as pe
    
    left join time_dim as tm
        on pe.timestamp_h = tm.time_stamp
    
    left join url_dim as u 
        on pe.url = u.url_full
    
    left join user_dim as us
        on pe.user = us.user_id
        
    left join postcode_dim as pc
        on us.current_postcode = pc.short_postcode
    
""")

#pageview fact table
insert_pageview_fact = ("""
insert into pageviews_fact (
    time_sk
    ,url_sk
    ,user_sk
    ,url_sk
    ,pageviews
    )
 
select 
    time_sk
    ,url_sk
    ,user_sk
    ,url_sk
    ,pageviews
    
    from pageview_stg
""")

#pageview fact table postcode update
update_pageview_fact = ("""
update pageviews_fact
    set pv.postcode_sk = pc.postcode_sk
    
    from pageviews_fact pv
    
    inner join user_dim as us
        on pv.user_sk = us.user_sk
        
    inner join postcode_dim as pc 
        on us.current_postcode = pc.short_postcode
        
    where pv.postcode_sk = 0
""")

#Query Lists

insert_dims_queries_hourly = ['tim_dim_insert', 'url_dim_insert', 'missing_users_insert']
insert_stg_queries_hourly = ['pageview_fact_stg_insert']

insert_fact_queries_hourly = ['insert_pageview_fact']

insert_queries_daily = ['user_dim_insert', 'postcode_dim_insert']
update_queries_daily = ['user_dim_update', 'update_pageview_fact']
