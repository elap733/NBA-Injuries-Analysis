# -*- coding: utf-8 -*-
"""
This script cleans www.basketball-reference.com 
for historical NBA team schedules. 

- Cleaning steps
    - Date formating
    
Outputs:
    - a 'master schedule' pickle dataframe that has the schedule
    "data" for  all teams. 

@author: evanl
"""

import pandas as pd
import pickle

#--------------------------User Inputs -----------------------
#scraped file path
scraped_filepath='../../data/01_raw/all_teams_schedule_2010_2020.csv'

#save path and output filename for pickle
savepath_pickle='../../data/02_cleaned/all_teams_schedule_2010_2020_cleaned.p'

#-------------------------Load Files-----------------------------------
#Read in previously scraped schedule Data
all_teams_sched_df = pd.read_csv(scraped_filepath,index_col = 0)

#---------------------Clean Data---------------------------------------------
    
#convert 'Date' to datetime format
all_teams_sched_df ['Date']=pd.to_datetime(all_teams_sched_df ['Date'],format='%a, %b %d, %Y', errors = 'coerce')
all_teams_sched_df ['Date']=pd.to_datetime(all_teams_sched_df ['Date'],infer_datetime_format=True)
    
#-------------------------Save Data-----------------------------
print('Saving files......')

#save 'master schedule' file as a pickle
pickle.dump(all_teams_sched_df, open(savepath_pickle, "wb" ) )

print('Finished')