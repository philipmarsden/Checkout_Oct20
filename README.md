# Checkout_Oct20
Checkout.com interview assignment


## Brief

Background
You have been asked to create a batch pipeline to take into consideration 2 sources of ingested
data, join them and deliver a denormalised table/model into Snowflake (or any other database
of your choice).

### Source Tables
#### Users
One of the sources consists of an operational database containing information about users. A
user has 2 properties:

- An id, uniquely identifying each user. Example: 1234
- A postcode, indicating where a user is at the moment. This attribute may change
regularly based on the user’s location. Example: SW19

We have an extract process which consumes the users’ data on a daily basis around midnight
(00:00). The process fully extracts users data, landing the data on a table within the Data
Warehouse named “users_extract”. This table is fully truncated/reloaded on each
execution

Volume: we have up to 20M users

#### Pageviews
The other source consists of an operational database containing information about pageviews
to a website. A pageview has 3 properties:
- A user_id, uniquely identifying a user. This matches the id on the users table. Example: 1234
- An url of the page being visited. Example: www.website.com/index.html
- A pageview_datetime when the pageview occurred. Example: 2019-10-11 14:55:23

We have an extract process which consumes the pageviews’ data on an hourly basis. The
process incrementally extracts pageviews data, landing the data on a table within the Data
Warehouse named “pageviews_extract”. On each execution of the extract process, this
table is fully truncated and subsequently loaded only with the pageviews data relative to the
previous hour.

Volume: on any given day, we may have 100M website pageviews


### Data Warehouse Model/Pipeline
Our end goal is to build the Data Warehouse tables/structures which will allow our BI tool to
easily and in a performant way answer 2 questions:

- Number of pageviews, on a given time period (hour, day, month, etc), per postcode -
based on the current/most recent postcode of a user.
- Number of pageviews, on a given time period (hour, day, month, etc), per postcode -
based on the postcode a user was in at the time when that user made a pageview.


# Data structure
We will build a star schema to house the underlying data, this shoudl provide a balance between efficiency
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
note - we can only really get the postcode as at midnight, rather than the preferred "when it changes" - determine
what value this will add and work with technology to see about how we can get a solution


- Page Views Fact Table: Count of the number of page views by time, user, url, and postcode at time of view (at 
least the postcode as at the last time it was recorded)
Fields: time_sk, url_sk, user_sk, postcode_sk, page_views (count)
Update: Hourly


