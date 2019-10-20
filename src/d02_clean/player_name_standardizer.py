# -*- coding: utf-8 -*-

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


@author: evanl
"""

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