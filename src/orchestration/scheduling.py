# code to schedule the sql jobs

import sys
import os
from locs import UPDATESPATH

from update_daily import *
from update_hourly import *

from apscheduler.schedulers.background import BackgroundScheduler

def daily_update ():
    update_daily.main()
    
def hourly_update():
    update_hourly.main()



def main ():

    scheduler = BackgroundScheduler()
    
    #add 2 jobs to the scheduler
    #daily update to run once per day
    #Ideally we will have a trigger, but set to 15 past midnight to allow for load time.
    #on the midnight run, the preference would be to have the daily run before the hourly so 
    #that the most recent location of useers is included.
    dailyjob = scheduler.addjob(daily_update, 'interval', days = 1)    

    #hourly job set to 5 past hour - 
    hourlyjob = scheduler.addjob(hourly_update, 'interval', hours = 1)
    
    #set up something to catch and check the QA code going into the jobfile. 
    #can we roll back the changes if they are not right or there is an error and try again.
    
    #set the scheduler running - this would be running constantly in the background on the server.
    scheduler.start()
    
    
