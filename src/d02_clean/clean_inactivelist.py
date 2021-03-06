# -*- coding: utf-8 -*-
"""
This script performs simple cleaning operations on Inactive List data scraped
using "inactivelist_scrape.py". It reads in a .csv containing scraped data and
saves this cleaned data as a pickled Pandas dataframe.

- Formats date
- Formats team names
- Formats names to match those in player stats; drops rows with missing data

Required Inputs:
   - 'prosportstransactions_scrape_IRL_2010_2019.csv'
   - 'teams_nickname_dictionary.p'
   - 'names_with_stats.p'
Outputs:
   - 'inactive_list_cleaned.p'

@author: evanl
"""
from player_name_standardizer import player_name_standardizer
import pandas as pd
import pickle

pd.set_option('display.expand_frame_repr', False)

#-----------------------------User Inputs------------------------------------

#path to scraped file
scraped_file_path = '../../data/01_raw/prosportstransactions_scrape_IRL_2010_2019.csv'

#save path and output filename
savepath='../../data/02_cleaned/inactive_list_cleaned.p'

#path to team nickname dictionary (used to standardize team names)
team_pickle_path = '../../references/01_dictionaries/teams_nickname_dictionary.p'

#path to Panda series of players with scraped player stats
names_file_path='../../data/02_cleaned/names_with_stats.p'

#-------------------------Load Files-----------------------------------

#Read in previously scraped Inactive List Data
inactive_list_df = pd.read_csv(scraped_file_path,index_col = 0)

#Read in team name dictionary (used to standardize team names)
team_name_dict = pickle.load(open( team_pickle_path, "rb" )) 

#Read in Panda series of player names with scraped player stats
names_with_stats_series = pickle.load(open(names_file_path, "rb" )) 

#-------------------Clean Data - Section 1: Format Date----------------------

#Change "Date" values from object data type to a date data type and sort data frame by date (past ---> present)
inactive_list_df['Date']=pd.to_datetime(inactive_list_df['Date'],infer_datetime_format=True)
inactive_list_df.sort_values(by = 'Date', inplace = True)
inactive_list_df.reset_index(drop = True, inplace = True)

#----------------- Clean Data - Section 2: Format Team Names------------------

#Change team name to full name with city and mascot
#Handle special cases first (same mascot, two different cities - New Jersey Nets, Brooklyn Net, New Orleans Hornets, Charlotte Hornets)
inactive_list_df.loc[((inactive_list_df['Team'] == 'Nets') & (inactive_list_df['Date'] <= pd.to_datetime('2012-06-18',infer_datetime_format=True))), 'Team'] = 'New Jersey Nets'
inactive_list_df.loc[((inactive_list_df['Team'] == 'Nets') & (inactive_list_df['Date'] >= pd.to_datetime('2012-06-18',infer_datetime_format=True))), 'Team'] = 'Brooklyn Nets'
inactive_list_df.loc[((inactive_list_df['Team'] == 'Hornets') & (inactive_list_df['Date'] <= pd.to_datetime('2013-06-18',infer_datetime_format=True))), 'Team'] = 'New Orleans Hornets'
inactive_list_df.loc[((inactive_list_df['Team'] == 'Hornets') & (inactive_list_df['Date'] >= pd.to_datetime('2013-06-18',infer_datetime_format=True))), 'Team'] = 'Charlotte Hornets'

#Map remaining teams to full team name using team_name_dict
inactive_list_df['Team'] = inactive_list_df['Team'].map(team_name_dict)

#Drop rows with no team name 
inactive_list_df.drop(index = inactive_list_df[inactive_list_df['Team'].isnull()].index, inplace = True)

##---------------Clean Data - Section 3: Format Player Names-------------------

#Check if any rows have a null for both "Acquired" and "Relinquished" columns; drop these rows
acquired_null_df = inactive_list_df[inactive_list_df['Acquired'].isnull()]
no_player_name_df = acquired_null_df[acquired_null_df['Relinquished'].isnull()]
inactive_list_df.drop(no_player_name_df.index, inplace = True)

#Separate out player names (some players have multiple names, each separated by a "/")
all_events_names = inactive_list_df['Acquired'].fillna('') + inactive_list_df['Relinquished'].fillna('')

aliases_df = all_events_names.str.split(pat = '/', expand = True)
aliases_df.columns = ['Player', 'Alt_name_1', 'Alt_name_2'] 

#Remove any strings in parentheses in player names (removes parentheses and the string within the parentheses)
aliases_df.replace(regex = ['\(.*?\)'], value = '', inplace = True)

#Remove suffixes on player names
aliases_df.replace(regex = ['Jr\.'], value = '', inplace = True)
aliases_df.replace(regex = ['III'], value = '', inplace = True)
aliases_df.replace(regex = ['IV'], value = '', inplace = True)

#Remove periods in player names
aliases_df['Player'].replace('\.', '', regex=True, inplace = True)
aliases_df['Alt_name_1'].replace('\.', '', regex=True, inplace = True)
aliases_df['Alt_name_2'].replace('\.', '', regex=True, inplace = True)

#Remove extra white spaces at the start or end of player names
aliases_df['Player']= aliases_df['Player'].str.strip()
aliases_df['Alt_name_1']= aliases_df['Alt_name_1'].str.strip()
aliases_df['Alt_name_2']= aliases_df['Alt_name_2'].str.strip()

#Make player name spelling consistent with those in scraped stats data
#Create a dictionary that will be used to map spellings
player_spelling_dict = player_name_standardizer(aliases_df,names_with_stats_series)

#Map panda series 'names_with_stats' player name spellings to 'missed_games_df'
aliases_df['Player'] = aliases_df['Player'].map(player_spelling_dict )
inactive_list_df['Player'] = aliases_df['Player']

#-----------------------Save Cleaned Data-----------------------------
print('Saving files......')

#save file
pickle.dump(inactive_list_df, open(savepath, "wb" ) )

print('Finished')