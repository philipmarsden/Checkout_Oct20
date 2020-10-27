
#view_list

create_view_queries = ['view_q1_create', 'view_q2_create']


#Question 1 - Number of pageviews, on a given time period (hour, day, month, etc), per postcode -
#based on the current/most recent postcode of a user.

view_q1_create = ("""
create view pageviews_by_current_postcode_v as
    select
        tm.time_stamp
        ,u.url_full
        ,us.current_postcode
        ,sum(pv.pageviews) as pageviews
        
    from pageviews_fact as pv
    
    left join time_dim as tm
        on pv.time_sk = tm.time_sk
        
    left join url_dim as u
        on pv.url_sk = u.url_sk
        
    left join user_dim as us
        on pv.user_sk = us.user_sk
        
    group by tm.time_stamp, u.url_full, us.current_postcode
""")

#Question 2 - Number of pageviews, on a given time period (hour, day, month, etc), per postcode -
#based on the postcode a user was in at the time when that user made a pageview.

view_q2_create = ("""
create view pageviews_by_postcode_v as 
    select
        tm.time_stamp
        ,u.url_full
        ,pc.short_postcode
        ,sum(pv.pageviews) as pageviews
        
    from pageviews_fact as pv
    
    left join time_dim as tm
        on pv.time_sk = tm.time_sk
        
    left join url_dim as u
        on pv.url_sk = u.url_sk
        
    left join postcode_dim as pc
        on pv.postcode_sk = pc.postcode_sk
        
    group by tm.time_stamp, u.url_full, pc.short_postcode
""")
