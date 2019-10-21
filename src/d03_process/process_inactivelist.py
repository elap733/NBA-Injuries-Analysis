# -*- coding: utf-8 -*-
"""

This script processes NBA Inactive List data that has been previously
scraped and cleaned (via "inactive_list_cleaned.py"). 

  Processing (feature engineering) steps:
    
      - Step 1 : Count of missed games for each "relinquished" inactive list event. 
        - Most events correspond to one missed game. Some events, particularily
        "DTD" (day-to-day) can correspond to several missed games. We can determine
        this exactly using schedule data. 
        
        Note: This part of the code takes a while to run.
    
      - Step 2 : Filter injury notes

  Inputs:
       - 'inactive_list_cleaned.p'
       - 'all_team_schedule_2010_2020.p'
  Outputs:
       - 'inactive_list_processed.p'

@author: evanl
"""
from correlate_event_to_game_schedule import correlate_event_to_game_schedule
from notes_filter import notes_filter
import pandas as pd
from datetime import timedelta
import pickle

pd.set_option('display.expand_frame_repr', False)

#--------------------------User Inputs---------- ----------------------
#path to scraped and cleaned inactive list events dataframe
IL_cleaned_pickle_path = '../../data/02_cleaned/inactive_list_cleaned.p'

#path to scraped, cleaned, and processed schedule data dataframe
teams_schedule_pickle_path = '../../data/03_processed/all_teams_schedule_2010_2020_processed.p'

#save path for pickle of inactive list event dataframe with feature engineering
savepath = '../../data/03_processed/inactive_list_processed.p'

#-------------------------Load Files-----------------------------------
#Read in previously scraped and cleaned inactive_list dataframe
inactive_list_df = pickle.load(open(IL_cleaned_pickle_path, "rb" )) 

#Read in previously scraped, cleaned, and processed schedule data
team_schedules_df = pickle.load(open(teams_schedule_pickle_path, "rb" )) 

#-----Processing - Section 1: Count Number of Missed Games--------
print('Counting number of missed games')

#Create a dataframe with only "Relinquished" events (e.g. player was placed on inactive list)
placed_on_IL_events_df = inactive_list_df[inactive_list_df['Acquired'].isnull()].copy()

placed_on_IL_events_df['Reg_games_missed'] = ''
placed_on_IL_events_df['Post_games_missed'] = ''
placed_on_IL_events_df['Out_for_season'] = ''
placed_on_IL_events_df['Season'] = ''
placed_on_IL_events_df['Year'] = ''
placed_on_IL_events_df['Game_number'] = ''

#Create a dataframe with only "Acquired" events (e.g. player was activated) 
acquired_events_df = inactive_list_df[inactive_list_df['Relinquished'].isnull()].copy()

acquired_events_df['Reg_games_missed'] = ''
acquired_events_df['Post_games_missed'] = ''
acquired_events_df['Out_for_season'] = ''
acquired_events_df['Season'] = ''
acquired_events_df['Year'] = ''
acquired_events_df['Game_number'] = ''

#Iterate over dataframe
for row in placed_on_IL_events_df.itertuples():
    
    date_placed_on_IL = row.Date
    game_number_placed_on_IL, game_date_placed_on_IL, season_placed_on_IL, year_placed_on_IL, team_total_num_games = correlate_event_to_game_schedule (team_schedules_df, row.Date, row.Team)
    
    #A flag to indicate if "placed on IL" event occurs on the first game of the season
    if (game_number_placed_on_IL == 1) & (season_placed_on_IL == 'regular'):
        start_of_season = 1
    else:
        start_of_season = 0 
        
    activated_events_df = inactive_list_df.loc[(inactive_list_df['Acquired'] == row.Relinquished) & inactive_list_df['Notes'].str.match('activated') & (inactive_list_df['Date'] > row.Date)]
    
    if not activated_events_df.empty: # An "activated" event exists 
        
        activated_events_df.reset_index(inplace = True)
        next_activated_event_df = activated_events_df.iloc[0,:]
        
        date_activated = next_activated_event_df['Date']    
        game_number_activated, game_date_activated, season_activated, year_activated, nothing = correlate_event_to_game_schedule (team_schedules_df, next_activated_event_df['Date'], next_activated_event_df['Team'])
    
        #calculate regular and post season games missed while on IL
        if season_placed_on_IL == 'regular': #Placed on IL during regular season
            if year_placed_on_IL == year_activated: #Reactivated during either regular or post season that same year
                out_for_season = 0 #flag for "placed on IL" events that result in the player being out for the remainder of the season (0 = FALSE, 1 = TRUE)
                if season_activated =='regular': #Ractivated during regular season of same year
                    regular_season_games_missed = game_number_activated - game_number_placed_on_IL
                    post_season_games_missed = 0
                elif (season_activated == 'post') & (year_placed_on_IL != 2011): #Ractivated during postseason (not 2011)
                    regular_season_games_missed = 82 - game_number_placed_on_IL
                    post_season_games_missed = game_number_activated - 82
                elif (season_activated == 'post') & (year_placed_on_IL == 2011): #Ractivated during 2011 postseason
                    regular_season_games_missed = 66 - game_number_placed_on_IL
                    post_season_games_missed = game_number_activated - 66 
            elif year_placed_on_IL != year_activated: #Not reactivated in regular or post season that same year
                out_for_season = 1 #flag for "placed on IL" events that result in the player being out for the remainder of the season
                if year_placed_on_IL != 2011:
                    regular_season_games_missed = 82 - game_number_placed_on_IL
                    post_season_games_missed = team_total_num_games - 82
                elif year_placed_on_IL == 2011:
                    regular_season_games_missed = 66 - game_number_placed_on_IL
                    post_season_games_missed = team_total_num_games - 66
        elif season_placed_on_IL == 'post': #Placed on IL during post season
            if year_placed_on_IL == year_activated: #Reactivated during post season that same year
                out_for_season = 0 #flag for "placed on IL" events that result in the player being out for the remainder of the season
                if (season_activated == 'post') & (year_placed_on_IL != 2011): #Ractivated during postseason (not 2011)
                    regular_season_games_missed = 0
                    post_season_games_missed = game_number_activated - game_number_placed_on_IL
                elif (season_activated == 'post') & (year_placed_on_IL == 2011): #Ractivated during 2011 postseason
                    post_season_games_missed = game_number_activated - game_number_placed_on_IL 
            elif year_placed_on_IL != year_activated: #Not reactivated post season that same year
                out_for_season = 1 #flag for "placed on IL" events that result in the player being out for the remainder of the season
                if year_placed_on_IL != 2011:
                    post_season_games_missed = team_total_num_games - game_number_placed_on_IL
                elif year_placed_on_IL == 2011:
                    post_season_games_missed = team_total_num_games - game_number_placed_on_IL
        elif season_placed_on_IL == 'off': #Placed on IL during off season
            out_for_season = 0 #flag for "placed on IL" events that result in the player being out for the remainder of the season
            regular_season_games_missed = 0
            post_season_games_missed = 0
    
    elif (activated_events_df.empty) & ('out for season' in row.Notes): # 'Activated' event does not exist, but notes includes text "out for season".
        out_for_season = 1 #flag for "placed on IL" events that result in the player being out for the remainder of the season
        if season_placed_on_IL == 'regular': #Placed on IL during regular season
            if year_placed_on_IL != 2011:
                regular_season_games_missed = 82 - game_number_placed_on_IL
                post_season_games_missed = team_total_num_games - 82
            elif year_placed_on_IL == 2011:
                regular_season_games_missed = 66 - game_number_placed_on_IL
                post_season_games_missed = team_total_num_games - 66
        elif season_placed_on_IL == 'post': #Placed on IL during post season
            if year_placed_on_IL != 2011:
                regular_season_games_missed = 0
                post_season_games_missed = team_total_num_games - game_number_placed_on_IL
            elif year_placed_on_IL == 2011:
                regular_season_games_missed = 0
                post_season_games_missed = team_total_num_games - game_number_placed_on_IL
        elif season_placed_on_IL == 'off': #Placed on IL during off season
            regular_season_games_missed = 0
            post_season_games_missed = 0
    elif activated_events_df.empty: # 'Activated' event does not exist, 
        regular_season_games_missed = ""
        post_season_games_missed = ""
        out_for_season = 1
    
    #update df
    placed_on_IL_events_df['Reg_games_missed'][row.Index] = regular_season_games_missed
    placed_on_IL_events_df['Post_games_missed'][row.Index] = post_season_games_missed
    placed_on_IL_events_df['Out_for_season'][row.Index] = out_for_season
    placed_on_IL_events_df['Season'][row.Index] = season_placed_on_IL
    placed_on_IL_events_df['Year'][row.Index] = year_placed_on_IL 
    placed_on_IL_events_df['Game_number'] [row.Index] = game_number_placed_on_IL 
    
#combine "acquired" and "relinquished" events into one data frame again
all_inactive_events_df= pd.concat([placed_on_IL_events_df, acquired_events_df])

#------------Processing - Section 2: Filter Notes --------------------
print('Filtering notes')
all_inactive_events_df['note_keyword'] = ''
all_inactive_events_df['category'] = ''

#apply notes_filter function to each row in dataframe
all_inactive_events_df[['note_keyword', 'category']]= all_inactive_events_df.apply(notes_filter, axis = 1, result_type="expand")

#-----------------------Save Data-----------------------------
print('Saving files......')
#save file
pickle.dump(all_inactive_events_df, open(savepath, "wb" ) )   
print('Finished')   