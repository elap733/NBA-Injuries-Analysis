# -*- coding: utf-8 -*-
"""
This script processes missed game data thats been previously scraped
and  cleaned (via "missed_games_cleaned.py"). Its read in this pickle  
and saves a new pickled Pandas dataframe with additional columns.

  Processing (feature engineering) steps:
    
      - Step 1: Count of missed games for each "relinquished" missed game event. 
        - Most events correspond to one missed game. Some events, particularily
        "DTD" (day-to-day) can correspond to several missed games. We can determine
        this exactly using schedule data. 
        
        Note: This part of the code takes a while to run.
    
       - Step 2 : Filter injury notes

  Inputs:
       - 'missed_games_cleaned.p'
       - 'all_team_schedule_2010_2020.p'
  Outputs:
       - 'missed_games_processed.p'
@author: evanl
"""

from correlate_event_to_game_schedule import correlate_event_to_game_schedule
from notes_filter import notes_filter
import pandas as pd
from datetime import timedelta
import pickle

pd.set_option('display.expand_frame_repr', False)


#--------------------------User Inputs---------- ----------------------
#path to scraped and cleaned missed game dataframe
mg_cleaned_pickle_path = '../../data/02_cleaned/missed_games_cleaned.p'

#path to scraped, cleaned, and processed schedule data dataframe
teams_schedule_pickle_path = '../../data/03_processed/all_teams_schedule_2010_2020_processed.p'

#save path for pickle of missed game dataframe with feature engineering
savepath = '../../data/03_processed/missed_games_processed.p'

#-------------------------Load Files-----------------------------------
#Read in previously scraped and cleaned Missed Game dataframe
missed_games_events_df = pickle.load(open(mg_cleaned_pickle_path, "rb" )) 

#Read in previously scraped, cleaned, and processed schedule data
team_schedules_df = pickle.load(open(teams_schedule_pickle_path, "rb" )) 

#-----Processing - Section 1: Count Number of Missed Games--------
print('Counting number of missed games')

missed_games_events_df['Reg_games_missed'] = ''
missed_games_events_df['Post_games_missed'] = ''
missed_games_events_df['Season'] = ''
missed_games_events_df['Year'] = ''
missed_games_events_df['Game_number'] = ''

##Iterate over dataframe
for row in missed_games_events_df.itertuples():
    
    date_mg_event = row.Date
    game_number_mg_event, game_date_mg_event, season_mg_event, year_mg_event, team_total_num_games = correlate_event_to_game_schedule (team_schedules_df, row.Date, row.Team)
    
    if 'DTD' in row.Notes: #if event is a "DTD" (day-to-day) event
        
        #find all missed games events for this player that happen after this event
        player_mg_events_df = missed_games_events_df.loc[((missed_games_events_df['Acquired'] == row.Relinquished) | (missed_games_events_df['Relinquished'] == row.Relinquished)) & (missed_games_events_df['Date'] > row.Date)]
        
        if not player_mg_events_df.empty: # If there are missed game events for this player after this event (e.g. dataframe is not empty) 
        
            player_mg_events_df.reset_index(inplace = True) # reset index
            next_player_mg_event_df = player_mg_events_df.iloc[0,:] # next missed game event for player
            
            if next_player_mg_event_df['Notes'] == 'returned to lineup':#if next mg event is a "returned to lineup" event
                
                #get game number,date,season, year of "returned to lineup"  (year should be the same; season may be different)    
                game_number_returned, game_date_returned, season_returned, year_returned, team_total_num_games = correlate_event_to_game_schedule (team_schedules_df, next_player_mg_event_df['Date'], next_player_mg_event_df['Team'])
                
                #Determine number of missed regular season and post season games
                if season_mg_event == 'regular': # if event occured in regular season
                    if (season_returned == 'regular') and (year_mg_event == year_returned): #if returned to lineup event occured in same regular season
                        regular_season_games_missed = game_number_returned - game_number_mg_event
                        post_season_games_missed = 0
                    elif (season_returned == 'post') and (year_returned != 2011) and (year_mg_event == year_returned): #return to lineup during postseason (not 2011)
                        regular_season_games_missed = 82 - game_number_mg_event
                        post_season_games_missed = game_number_returned - 82
                    elif (season_returned == 'post') and (year_returned == 2011) and (year_mg_event == year_returned): #return to lineup during 2011 postseason
                        regular_season_games_missed = 66 - game_number_mg_event
                        post_season_games_missed = game_number_returned - 66 
                    else: 
                        print('hmm...bad data?')
                if season_mg_event == 'post': # if event occured in post season
                    if (season_returned == 'post') and (year_mg_event == year_returned):
                        regular_season_games_missed = 0
                        post_season_games_missed = game_number_returned - game_number_mg_event                      
                    else:
                        print('hmm...bad data?')
             
            else: # if next mg event is not "returned to lineup" then assume just one game missed
                if season_mg_event == 'regular': # if event occured in regular season                        
                    regular_season_games_missed = 1
                    post_season_games_missed = 0  
                if season_mg_event == 'post': # if event occured in regular season                        
                    regular_season_games_missed = 0
                    post_season_games_missed = 1  
        else: #if there are no mg events after this event then assume just one game missed
            if season_mg_event == 'regular': # if event occured in regular season                        
                regular_season_games_missed = 1
                post_season_games_missed = 0  
            if season_mg_event == 'post': # if event occured in regular season                        
                regular_season_games_missed = 0
                post_season_games_missed = 1  
    elif 'returned to lineup' not in row.Notes: #mg event is not a return to lineup event or a 'DTD' event
        if season_mg_event == 'regular': # if event occured in regular season                        
            regular_season_games_missed = 1
            post_season_games_missed = 0  
        if season_mg_event == 'post': # if event occured in regular season                        
            regular_season_games_missed = 0
            post_season_games_missed = 1
        if season_mg_event == 'off': # if event occured in off season                        
            regular_season_games_missed = 0
            post_season_games_missed = 0 
    elif 'returned to lineup'  in row.Notes: #mg event is a return to lineup event
        regular_season_games_missed = 0
        post_season_games_missed = 0  
 
    #update df
    missed_games_events_df['Reg_games_missed'][row.Index] = regular_season_games_missed
    missed_games_events_df['Post_games_missed'][row.Index] = post_season_games_missed
    missed_games_events_df['Season'][row.Index] = season_mg_event
    missed_games_events_df['Year'][row.Index] = year_mg_event
    missed_games_events_df['Game_number'] = game_number_mg_event

#------------Processing - Section 2: Filter Notes --------------------
print('Filtering notes')
missed_games_events_df['note_keyword'] = ''
missed_games_events_df['category'] = ''

#apply notes_filter function to each row in dataframe
missed_games_events_df[['note_keyword', 'category']]= missed_games_events_df.apply(notes_filter, axis = 1, result_type="expand")

#-----------------------Save Data-----------------------------
print('Saving files......')
#save file
pickle.dump(missed_games_events_df, open(savepath, "wb" ) )        
print('Finished')   