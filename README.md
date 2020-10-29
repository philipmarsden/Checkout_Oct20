# Checkout_Oct20
Checkout.com interview assignment

## Brief

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


### repostory structures

.
* config \ for config & connection files
* documentation \ all documentation on process and data
* src \ source code
	* etl \ pipeline code 
	* orchestration \ scheduling code
	* schema \ inital table create
	* test \ job tracker and insert
	* views \ non-physical layer to answer questions


### Thoughts for Future 

potential issues:
- need to check the pageviews data in the extract to see the start and end time - can the hours overlap?
- what happens when a user has a pageview in the time between the start of the hour and extract and then the same pageview
within the next hour?
can separate them off and union with next hours load - so that 1 hour is loaded in full at a time.

- Adding in new variables - how can we do this efficiently.
dev > test > prod - how long does this process take? - agile delivery every 2 weeks?
how do we expand out the dimensions with additional fact tables and data 

- how can we leverge these tables for other tasks. e.g. users table - this can be improved and used quickly for value adding analytics.
Make sure this is our golden source for users. 

- long term how does this scale? data volumes expected to grow, company is scalaing v quickly and so volumes could double in < 12m.
increase processing power - cloud setup means this is possible at a cost.
how can we make it more efficient - collecting addtional data at source? e.g. postcode at time of view?



