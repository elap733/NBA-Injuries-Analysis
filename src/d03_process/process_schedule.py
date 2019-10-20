# -*- coding: utf-8 -*-
"""
This script processes www.basketball-reference.com 
for historical NBA team schedules. 

- Processing steps
    - Add 'season' (regular, post) for each game
    - Modify 'Away_flag'
    - Reorder columns
    
Required Inputs:
   - 'all_teams_schedule_2010_2020_cleaned.p'

Outputs:
   - 'all_teams_schedule_2010_2020_processed.p'

@author: evanl
"""

import pandas as pd
import pickle

#--------------------------User Inputs -----------------------
#cleaned file path
cleaned_filepath='../../data/02_cleaned/all_teams_schedule_2010_2020_cleaned.p'

#save path and output filename for pickle
savepath_pickle='../../data/03_processed/all_teams_schedule_2010_2020_processed.p'

#-------------------------Load Files-----------------------------------
#Read in previously cleaned schedule Data
all_teams_sched_df = pd.read_csv(cleaned_filepath,index_col = 0)

#-------------------Process Data - Step 1: Add 'season'-----------------------
    
#add a column indicating the season (regular, post)
all_teams_sched_df['Season'] = ''

for row in all_teams_sched_df.itertuples():
    if row.Year != '2011':
        if row.Game_num <= 82:
            all_teams_sched_df['Season'] = 'regular'
        else: 
            all_teams_sched_df['Season'] = 'post'
    else:
        if row.Game_num <= 66:
           all_teams_sched_df['Season'] = 'regular'
        else: 
           all_teams_sched_df['Season'] = 'post'
            

#-------------------Process Data - Step 2: Modify 'Away_flag'-----------------------

#modify "Away_flag" column; "@" = 1, null = 0
all_teams_sched_df['Away_flag']=all_teams_sched_df['Away_flag'].map({'@':1,'': 0})

#reorder columns
all_teams_sched_df = all_teams_sched_df[['Team','Year', 'Season', 'Game_num','Date','Away_flag','Opponent','OT_flag']]
    
#-------------------------Save Data-----------------------------
print('Saving files......')

#save 'master schedule' file as a pickle
pickle.dump(all_teams_sched_df, open(savepath_pickle, "wb" ) )

print('Finished')