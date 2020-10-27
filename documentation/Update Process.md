
### Scheduler

We have used python scheduler - other options may be better but this is simple and easily installed.
https://apscheduler.readthedocs.io/en/stable/userguide.html#basic-concepts

Other options to operate at scale may be something like airflow which has useful user interface for managing many pipelines. 
I have some, but limited, experience with airflow and so have not tried to implement it here.


## Stages of the process

There is an assumption that the data will be archived off into cold storage by another process and so that is out of scope here.
we have a daily update and an hourly update.

daily:
copy of the user table with postcode as at time of extract. c. 20m records

Each day we need to update the users table with the most recent data
It is possible that we have a user in the pageviews table if they are a new user and view a page in the same day
in these cases we have created a dummy postcode variable which can be overwritten the next morning with the most recent postcode we have

1. insert the new users into the table
2. update all users with the most recent post code
3. update the previous fact table where dummy postcodes exist


hourly:
page views for the previous hour - not a perfect hour, but the time since the last run. probably about 5m records

1. Update the dimensions. Time, url, any new user as above with a dummy postcode
2. summarise the extract to hour, url, user, postcode
3. using the updated dimenstions add in the surrogate keys
4. load the new data into the fact table

