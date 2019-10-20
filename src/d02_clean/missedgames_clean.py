# -*- coding: utf-8 -*-
"""
This script performs simple cleaning operations on missed game data scraped
using "missedgames_scrape.py". It reads in a .csv containing scraped data and
saves this cleaned data as a pickled Pandas dataframe.

- Formats date
- Formats team names
- Formats names to match those in player stats; drops rows with missing data

@author: evanl
"""
import pandas as pd
import pickle

pd.set_option('display.expand_frame_repr', False)

#-----------------------Define Functions--------------------------------------

def player_name_standardizer(aliases_df,names_with_stats_series):

    """ This function standardizes player name spelling. The spelling of player 
    names in the 'aliases_df' dataframes may not match those
    found in the 'names_with_stats_series' pandas series. The 'aliases_df'
    contain up to three different spellings for each player's name 
    (columns 'Player', 'Name_alt_1', Name_alt_2'). This function finds which of these
    three names matches the player name in the 'names_with_stats_series'. 
    
    Input: aliases_df; names_with_stats_series
    
    Output: a dictionary for standardizing spelling. Keys are player names found
    in 'Player' column in 'aliases_df'. Value is corresponding spelling of 
    player name in 'names_with_stats_series'. If no match is found, 'No Match'
    is the value.
    
    Use this dicitionary to standardize player spellings

    """

    aliases_unique_player_df = aliases_df.drop_duplicates('Player')
    aliases_unique_player_df['Name_to_use'] = ''

    ps_unique_player_series = names_with_stats_series

    for row in aliases_unique_player_df.itertuples():
        if not ps_unique_player_series[ps_unique_player_series.isin([row.Player])].empty:
            aliases_unique_player_df['Name_to_use'][row.Index] = row.Player
        elif ps_unique_player_series[ps_unique_player_series.isin([row.Player])].empty:
            if not ps_unique_player_series[ps_unique_player_series.isin([row.Alt_name_1])].empty:
                aliases_unique_player_df['Name_to_use'][row.Index] = row.Alt_name_1
            elif ps_unique_player_series[ps_unique_player_series.isin([row.Alt_name_1])].empty:  
                if not ps_unique_player_series[ps_unique_player_series.isin([row.Alt_name_2])].empty:
                    aliases_unique_player_df['Name_to_use'][row.Index] = row.Alt_name_2
                elif ps_unique_player_series[ps_unique_player_series.isin([row.Alt_name_2])].empty:
                    aliases_unique_player_df['Name_to_use'][row.Index] = 'No Match'
        else:
            aliases_unique_player_df['Name_to_use'][row.Index] = 'No Match'
            
    name_dictionary = dict(zip(aliases_unique_player_df.Player, aliases_unique_player_df.Name_to_use))
    
    return name_dictionary

#--------------------------User Inputs---------- ----------------------
#path to scraped file
scraped_file_path = 'C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/Missed Games/prosportstransactions_scrape_missedgames_2010_2019.csv'

#save path and output filename
savepath='C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/Missed Games/missed_games_cleaned.p'

#path to team nickname dictionary (used to standardize team names)
team_pickle_path = 'C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/teams_nickname_dictionary.p'

#path to Panda series of players with scraped player stats
names_file_path='C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/Player Stats/names_with_stats.p'

#-------------------------Load Files-----------------------------------
#Read in previously scraped Missed Game Data
missed_games_df = pd.read_csv(scraped_file_path,index_col = 0)

#Read in team name dictionary (used to standardize team names)
team_name_dict = pickle.load(open( team_pickle_path, "rb" )) 

#Read in Panda series of player names with scraped player stats
names_with_stats_series = pickle.load(open(names_file_path, "rb" )) 

#-------------------Clean Data - Section 1: Format Date----------------------

#Change "Date" values from object data type to a date data type and sort data frame by date (past ---> present)
missed_games_df['Date']=pd.to_datetime(missed_games_df['Date'],infer_datetime_format=True)
missed_games_df.sort_values(by = 'Date', inplace = True)
missed_games_df.reset_index(drop = True, inplace = True)

#----------------- Clean Data - Section 2: Format Team Names------------------

#Change team name to full name with city and mascot
#Handle special cases first (same mascot, two different cities - New Jersey Nets, Brooklyn Net, New Orleans Hornets, Charlotte Hornets)
missed_games_df.loc[((missed_games_df['Team'] == 'Nets') & (missed_games_df['Date'] <= pd.to_datetime('2012-06-18',infer_datetime_format=True))), 'Team'] = 'New Jersey Nets'
missed_games_df.loc[((missed_games_df['Team'] == 'Nets') & (missed_games_df['Date'] >= pd.to_datetime('2012-06-18',infer_datetime_format=True))), 'Team'] = 'Brooklyn Nets'
missed_games_df.loc[((missed_games_df['Team'] == 'Hornets') & (missed_games_df['Date'] <= pd.to_datetime('2013-06-18',infer_datetime_format=True))), 'Team'] = 'New Orleans Hornets'
missed_games_df.loc[((missed_games_df['Team'] == 'Hornets') & (missed_games_df['Date'] >= pd.to_datetime('2013-06-18',infer_datetime_format=True))), 'Team'] = 'Charlotte Hornets'

#Map remaining teams to full team name using team_name_dict
missed_games_df['Team'] = missed_games_df['Team'].map(team_name_dict)

#Drop rows with no team name 
missed_games_df.drop(index = missed_games_df[missed_games_df['Team'].isnull()].index, inplace = True)

##---------------Clean Data - Section 3: Format Player Names-------------------

#Check if any rows have a null for both "Acquired" and "Relinquished" columns; drop these rows
acquired_null_df = missed_games_df[missed_games_df['Acquired'].isnull()]
no_player_name_df = acquired_null_df[acquired_null_df['Relinquished'].isnull()]
missed_games_df.drop(no_player_name_df.index, inplace = True)

#Separate out player names (some players have multiple names, each separated by a "/")
all_events_names = missed_games_df['Acquired'].fillna('') + missed_games_df['Relinquished'].fillna('')

aliases_df = all_events_names.str.split(pat = '/', expand = True)
aliases_df.columns = ['Player', 'Alt_name_1', 'Alt_name_2'] 

#Remove any strings in parentheses in player names
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
missed_games_df['Player'] = aliases_df['Player']

#-----------------------Save Cleaned Data-----------------------------
print('Saving files......')

#save file
pickle.dump(missed_games_df, open(savepath, "wb" ) )

print('Finished')