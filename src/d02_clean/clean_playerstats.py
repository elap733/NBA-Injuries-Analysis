# -*- coding: utf-8 -*-
"""
This script performs simple cleaning operations on player stats scraped
using "playerstats_scrape.py". It reads in a .csv containing scraped data and
saves this cleaned data as a pickled Pandas dataframe.

- Format player names (remove accents,periods, white space)
- Formats team names (full name - city and mascot)
- Drops rows with missing data
- Drops columns that will not be used
- Formats column names

Required Inputs:
   - 'player_stats_1994_2019.csv'
   - 'teams_abrv_dictionary.p'
   - 'names_with_stats.p'
Outputs:
   - 'player_stats_cleaned.p'

@author: evanl
"""
import pandas as pd
import pickle
import unicodedata

pd.set_option('display.expand_frame_repr', False)

#-----------------------Define Functions------------------------------
def strip_accents(s):
   
    """
    This function removes accents from characters within a string, replacing those 
    characters with a non-accented unicode character. Input is a string. 
    Output is a string.
    """
    
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

#--------------------------User Inputs---------- ----------------------
#path to scraped file
scraped_file_path = '../../data/01_raw/player_stats_1994_2019.csv'

#save path and output filename for dataframe with player stats
stats_savepath='../../data/02_cleaned/player_stats_cleaned.p'

#path to Panda series of players with scraped player stats
names_savepath='../../data/02_cleaned/names_with_stats.p'

#path to team abbreviation dictionary (used to standardize team names)
team_pickle_path = '../../references/01_dictionaries/teams_abrv_dictionary.p'

#-------------------------Load Files-----------------------------------
#Read in previously scraped player stats
player_stats_df = pd.read_csv(scraped_file_path,index_col = 0)

#Read in team name dictionary (used to standardize team names)
team_name_dict = pickle.load(open( team_pickle_path, "rb" )) 

#------------------------Clean Scraped Data-----------------------------

#Clean up player names; strip accents; remove '*' at the end of some player names
player_stats_df['Player'] = player_stats_df['Player'].apply(strip_accents)
player_stats_df['Player'] = player_stats_df['Player'].replace(regex = ['\*'], value = '')

#Remove periods in player names
player_stats_df['Player'].replace('\.','', regex=True, inplace = True)

#Remove extra white spaces at the start or end of player names
player_stats_df['Player']= player_stats_df['Player'].str.strip()

#Map remaining teams to full team name using team_name_dict
player_stats_df['Tm'] = player_stats_df['Tm'].replace(team_name_dict)

#Drop columns that won't be used in this analysis
player_stats_df.drop(['FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%','ORB', 'DRB', 'TRB', 'AST' , 'STL', 'BLK', 'TOV', 'PF', 'PTS'], axis = 1, inplace = True)

#Change column names
player_stats_df.columns = ['Year', 'Season', 'Player', 'Pos', 'Age', 'Team', 'G', 'GS', 'MPPG'] 

#Create a panda series containing unique player names
player_stats_unique_player_df = player_stats_df.drop_duplicates('Player')
player_names_series = player_stats_unique_player_df['Player']

#-----------------------Save Cleaned Data-----------------------------
print('Saving files......')

#save file with player stats
pickle.dump(player_stats_df, open(stats_savepath, "wb" ) )

#save file with unique player names 
pickle.dump(player_names_series, open(names_savepath, "wb" ) )

print('Finished')