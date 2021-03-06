## Data structure
We will build a star schema to house the underlying data, this should provide a balance between efficiency
and flexibility when it comes to running queries. 
If we find that the database is not performant then consider changing to something more like cassandra tables
with each query having a specific table and columnar format should provide improved speed.
I have not done that here as i would also like to be more forward thinking and allow for a degree of self serve
capabilities, where ad-hoc queries can be answered by the business rather than the data team needing to build 
bespoke tables for each question.


### Star Schema structure
#### Dimensions
- Time: one row per hour - currently based on exisitng timestamps however could be updated in future to include
all hours if needed. 
Fields: time_sk, timestamp, year, month, week, day, hour
Update: Hourly

- URL: one row per unique url - This will contain information on the URLs visited.
Fields: url_sk, url_full
Future potential: company ownership, page type, domain groupings
Update: Hourly

- Postcode: one row per short postcode: short postcode is the first section e.g. SW19. Preference
here would be to get an official full list from governmental sources, but for now we will use only
those captured.
Fields: postcode_sk, short_postcode
Future potential: country, county
Update: Daily

- Users: one row per user - most recent user data only. No personally identifiable information to be stored
Fields: user_sk, user_id, current_postcode 
Update: Daily
note - this is likely to be where performance is tested in having a dimension with 20m rows. This will impact the 
second question looking at current location. If the issue presents then we will brainstorm solutions.
note (assumption) - we can only really get the postcode as at midnight, rather than the preferred "when it changes" - determine
what value this will add and work with technology to see about how we can get a solution

- Page Views Fact Table: Count of the number of page views by time, user, url, and postcode at time of view (at 
least the postcode as at the last time it was recorded)
Fields: time_sk, url_sk, user_sk, postcode_sk, page_views (count)
Update: Hourly


### Views to answer questions
- Number of pageviews, on a given time period (hour, day, month, etc), per postcode -
based on the current/most recent postcode of a user.
-- Summary of the fact table with a join on user to get the current postcode
pageviews_by_current_postcode_v

- Number of pageviews, on a given time period (hour, day, month, etc), per postcode -
based on the postcode a user was in at the time when that user made a pageview.
-- Summary of the fact table taking the postcode stored within fact table
pageviews_by_postcode_v