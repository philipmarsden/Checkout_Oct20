
# Testing

## Built in QA checks
i have created a job table to track the updates and to make sure that they have completed correctly
in future build in some error handling to roll back changes and try again if a job has not completed
(this may be a feature in scheduling tools)

- job_id 
- starttime 
- endtime
- job_type
- expected_rows 
- inserted_rows 
- null_values
- completed

#### Integrity
#### Integrity
check volumes

users - total users in extract. total users in db
new pageviews - check number today. total in db hourly - existing number in db hourly
				check recent hour. total in db recnt hour
				
check for missing values
	any nulls in fact table - should be zero
	
	
#### Performance
how long did it take
	record of starttime, endtime
	
This is to make sure that the process remains performant as we scale, when we start to see a deterioration in
time then we may need to re-think our approach.
	
	
## syntax and process testing
as we make implement and make changes to the process we will need to run a small amount of fake data through the process
the assumption is that we have a live environment and a testing environment

we would build the proposed model in the test environment, then promote to live once it has passed a series of checks.
These would be similar to the QA checks we have built in to flag up if anything was going wrong.

typical things I would check

- row counts in = row counts out
- data types are correct
- missing values

