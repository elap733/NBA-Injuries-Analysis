# -*- coding: utf-8 -*-
"""
This script processes player stats data thats been previously scraped
and cleaned (via "player_stats_cleaned.py"). 

  Processing (feature engineering) steps:
    
      - Step 1 : For a given player and season calcualtes:
          - Total minutes played in current season
          - Total minutes played in prior seasons
          - Total games played in current season
          - Total games played in prior seasons
        
  Required Inputs:
       - 'player_stats_cleaned.p'
       - 'all_team_schedule_2010_2020.p'
  Outputs:
       - 'player_stats_processed.p'

@author: evanl
"""

import pandas as pd
import pickle

pd.set_option('display.expand_frame_repr', False)


#--------------------------User Inputs---------- ----------------------
#path to scraped and cleaned player stats dataframe
ps_cleaned_pickle_path = '../../data/02_cleaned/player_stats_cleaned.p'

#path to scraped, cleaned, and processed schedule data dataframe
teams_schedule_pickle_path = '../../data/03_processed/all_teams_schedule_2010_2020_processed.p'

#save path for pickle of player stats dataframe with feature engineering
savepath =  '../../data/03_processed/player_stats_processed.p'

#-------------------------Load Files-----------------------------------
#Read in previously scraped and cleaned Missed Game dataframe
all_player_stats_df = pickle.load(open(ps_cleaned_pickle_path, "rb" )) 

#Read in previously scraped, cleaned, and processed schedule data
team_schedules_df = pickle.load(open(teams_schedule_pickle_path, "rb" )) 


#-----Feature Engineering - Section 1: Total Minutes and Games Played---------

""" This section calculates the following for each player in each season 
(regular/post)/year they were active:
    
- Total games played in PRIOR seasons (TGP_prior_seasons)
- Total minutes played in PRIOR seasons (TMP_prior_seasons)
- Total minutes played in CURRENT season (TMP_current_season)

"""
#Handle cases where a player has multipe entries for a given regular season. This
#occurs when the player is traded mid season. There is a row for their time with
#each team and one where 'Tm' == "TOT" (this row contains totals across all teams 
#for that season. We want to keep just the row containing totals.)

rows_to_drop_df = all_player_stats_df[all_player_stats_df.duplicated(subset = ['Year','Player','Season'], keep = 'first')] #Find  rows which have the same 'year', 'player', and 'season-type'; keep the "first" occurence which corresponds to the row containing "TOT"
row_indices_to_drop = rows_to_drop_df.index
all_player_stats_df.drop(row_indices_to_drop, inplace = True) # drop rows

unique_player_names = all_player_stats_df['Player'].unique() #get a list of unique player names

for name in unique_player_names: #loop through each player
    
    #find all rows correspoding to player
    single_player_stats_df = all_player_stats_df[all_player_stats_df['Player'] == name].copy()  
    
    #calculate total games played in prior seasons
    single_player_stats_df['TGP_prior_seasons'] = single_player_stats_df['G'].cumsum() - single_player_stats_df['G']
    
    #calculate minutes played in current season and total minutes played in prior seasons
    single_player_stats_df['TMP_current_season'] = single_player_stats_df['MPPG']*single_player_stats_df['G']
    single_player_stats_df['TMP_prior_seasons'] = single_player_stats_df['TMP_current_season'].cumsum() - single_player_stats_df['TMP_current_season']
    
    #update original dataframe 
    all_player_stats_df.loc[single_player_stats_df.index, 'TGP_prior_seasons'] =  single_player_stats_df['TGP_prior_seasons']
    all_player_stats_df.loc[single_player_stats_df.index, 'TMP_current_season'] =  single_player_stats_df['TMP_current_season']
    all_player_stats_df.loc[single_player_stats_df.index, 'TMP_prior_seasons'] =  single_player_stats_df['TMP_prior_seasons']


#-----------------------Save Data-----------------------------
print('Saving files......')

#save file
pickle.dump(all_player_stats_df, open(savepath, "wb" ) )              

print('Finished')