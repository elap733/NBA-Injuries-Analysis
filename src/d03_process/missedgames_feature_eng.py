# -*- coding: utf-8 -*-
"""
This script performs feature engineering on missed game data thats been scraped
and partially cleaned ("missed_games_cleaned.py"). Its read in this pickle  
and saves a new pickled Pandas dataframe with additional columns.

Feature Engineering
- Count of missed games for each "relinquished" missed game event. 
    - Most events correspond to one missed games. Some events, particularily
    "DTD" (day-to-day) can correspond to several missed games. We can determine
    this exactly using schedule data.
- Filter injury notes

@author: evanl
"""

import pandas as pd
from datetime import timedelta
import pickle

pd.set_option('display.expand_frame_repr', False)

"""---------------------Define Functions ------------------------------"""

def correlate_event_to_game_schedule (team_schedules_df, event_date, event_team): 
    
    """
    This function finds the nearest scheduled NBA game to a missed game (MG)/
    inactive list (IL) event. In many cases the event date corresponds exactly
    with a scheduled game (this almost always the case for MG events). In cases
    where it does not however, we must find the first game that occurs after 
    the event. This function has three inputs: the team_schedules_df, date placed on IL, player's team.
    Output is: the game number closest to the IL event , a season type
    ('regular', 'post', 'off'), the season year, and the number of post season
    games the team played in that season year.
    """
    
    sched_on_after_event_df = team_schedules_df.loc[(team_schedules_df['Date'] >= event_date) & (team_schedules_df['Team'] == event_team)] #slice team_schedules_df to those games that occured on or after event (only include games for team of interest)
    
    if sched_on_after_event_df.empty: #empty dataframe means event occured in offseason in between a team name/city change
        team_name_change_dict = {
                'Charlotte Bobcats': 'Charlotte Hornets',
                'New Jersey Nets': 'Brooklyn Nets',
                'New Orleans Hornets': 'New Orleans Pelicans',
                }
        event_team = team_name_change_dict[event_team] #change team name
        
        sched_on_after_event_df = team_schedules_df.loc[(team_schedules_df['Date'] >= (event_date)) & (team_schedules_df['Team'] == event_team)]
        
    sched_on_after_event_df.reset_index(inplace = True) #rest df index
    closest_game_to_event_df = sched_on_after_event_df.iloc[0,:] #first row in dataframe corresponds to the game that is closest to (on or after) the event
      
    ## Identify game number corresponding to  event ##
    game_number = closest_game_to_event_df['Game_num'] #Game number go from 1-82 for regular season games (exception is strike shortened 2011 season)
    game_date = closest_game_to_event_df['Date']
    
    # Identify season and year in which event occured ##
    if game_number != 1: # Event occured during the regular or post season
        season = closest_game_to_event_df['Season']
        year = closest_game_to_event_df['Year']
    elif (game_number == 1) & ((event_date == closest_game_to_event_df['Date']) or (event_date ==(closest_game_to_event_df['Date'] - timedelta(days=1)))): #event occured on either the day before the first day of the season or on the first day of the season
        season = closest_game_to_event_df['Season']
        year = closest_game_to_event_df['Year']
    else: #event occured in off season 
        season = 'off'
        year = str(int(closest_game_to_event_df['Year'])-1)
        
    ##Find the total number of games the team played in during this season
    team_total_num_games = team_schedules_df[(team_schedules_df['Team']==event_team) & (team_schedules_df['Season'] == season) & (team_schedules_df['Year'] == year)]['Game_num'].max()
   
    return game_number, game_date, season, year, team_total_num_games

def notes_filter(c):
    
    """
    This function filters the "notes" field associated with each missed game
    or inactive list event. It returns: (a)  "note keyword" (e.g. calf, shin),
    and (b) a note "category" (eg. lower leg sick, healthy inactive)
    """
    
    #convert string to lower case characters
    note = c['Notes']
    lower_case_note =note.lower()
    
    #-------------Player activated or returned to lineup----------------------
    if any(x in lower_case_note for x in ['return', 'returned','activate', 'activated']):
        return 'returned to lineup', 'n/a'
               
    #----------Healthy Inactive/Missed Game--------------------------
    #If no reason is given for missed game or move to inactive list, assume it
    #was a non-injury move.
    elif lower_case_note == 'placed on il' or lower_case_note == 'placed on il (p)':
        return 'roster move', 'healthy inactive'
    
    elif 'suspension' in lower_case_note:
        return 'suspension', 'healthy inactive'
    
    elif any(x in lower_case_note for x in ['family','personal','birth', 'death']):
        return 'personal reasons', 'healthy inactive'
    
        
    #-------Rest Inactive--------------------------------
    elif 'rest' in lower_case_note:
        return 'rest', 'rest'
           
     #-------Sick Inactive  -------------------------------
    elif any(x in lower_case_note for x in ['virus','headache','flu', 'sick', 'illness','infection','pneumonia', 'gastro','appende','nausea', 'pox', 'dizziness', 'poisoning','bronchitis']):
        return 'sick', 'sick'
    
    #--------Foot Injuries------------------------------------
    elif 'foot' in lower_case_note:
        return 'foot', 'foot'
    elif 'toe' in lower_case_note:
        return 'toe', 'foot'
    elif 'heel' in lower_case_note:
        return 'heel', 'foot'
    
    #-------Lower leg injuries---------------------------
    elif 'ankle' in lower_case_note:
        return 'ankle', 'lower leg'             
    elif 'achilles'in lower_case_note:
        return 'achilles', 'lower leg'  
    elif 'calf' in lower_case_note:
        return 'calf', 'lower leg'
    elif 'shin' in lower_case_note:
        return 'shin', 'lower leg'
    elif 'tibia' in lower_case_note:
        return 'tibia', 'lower leg'
    elif 'fibula' in lower_case_note:
        return 'fibula','lower leg'
   
    #---------Knee injuries------------------------------------
    elif 'acl' in lower_case_note:
        return 'ACL', 'knee'
    elif 'mcl' in lower_case_note:
        return 'MCL', 'knee'
    elif any(x in lower_case_note for x in ['knee','patella','meniscus']):
        return 'knee', 'knee'
    
    #---------Upper leg injuries---------------------------------
    elif any(x in lower_case_note for x in ['quad','quadriceps','thigh']):
        return 'quad', 'upper leg'
    elif 'hamstring' in lower_case_note:
        return 'hamstring', 'upper leg'
    elif 'groin' in lower_case_note:
        return 'groin', 'upper leg'
    elif any(x in lower_case_note for x in ['hip','adductor']):
        return 'hip', 'upper leg'
    elif 'femur' in lower_case_note:
        return 'femur', 'upper leg'
    
    #-----------leg catch all------------------------------------
    elif 'leg' in lower_case_note:
        return 'leg', 'leg'
    
    
    #-----------Torso injuries--------------------------
    elif any(x in lower_case_note for x in ['chest', 'pectoral']):
        return 'chest', 'torso'
    elif any(x in lower_case_note for x in ['shoulder','rotator cuff']):
        return 'shoulder', 'torso'
    elif 'back' in lower_case_note:
        return 'back', 'torso'
    elif 'collarbone' in lower_case_note:
        return 'collarbone', 'torso'
    elif 'rib' in lower_case_note:
        return 'ribs', 'torso'
    elif any(x in lower_case_note for x in ['abdom','abductor','oblique']):
        return 'abdominal', 'torso'
    
    #------------Head/neck injuries----------------------------
    elif 'neck' in lower_case_note:
        return 'neck', 'head'
    elif any(x in lower_case_note for x in ['head', 'concussion']):
        return 'head', 'head'
    elif 'eye' in lower_case_note:
        return 'eye', 'head'
    elif 'nose' in lower_case_note:
        return 'nose', 'head'
    
    #------------ Hand injuries---------------------------------
    elif 'hand' in lower_case_note:
        return 'hand', 'hand'
    elif any(x in lower_case_note for x in ['finger', 'thumb']):
        return 'finger', 'hand'

    
    #------------ Arm injuries---------------------------------
    elif 'arm' in lower_case_note:
        return 'arm', 'arm'
    elif 'elbow' in lower_case_note:
        return 'elbow', 'arm'
    elif 'bicep' in lower_case_note:
        return 'bicep', 'arm'
    elif 'tricep' in lower_case_note:
        return 'tricep', 'arm'
    elif 'wrist' in lower_case_note:
        return 'wrist', 'arm'     
    else:
        return 'other', 'other'

""" --------------------Main----------------------------------------"""

#--------------------------User Inputs---------- ----------------------
#path to scraped and cleaned missed game dataframe
mg_cleaned_pickle_path = 'C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/Missed Games/missed_games_cleaned.p'

#path to scraped, cleaned, and processed schedule data dataframe
teams_schedule_pickle_path = 'C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/Schedules/all_teams_schedule_2010_2020.p'

#save path for pickle of missed game dataframe with feature engineering
savepath = 'C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/Missed Games/missed_games_feature_eng.p'

#-------------------------Load Files-----------------------------------
#Read in previously scraped and cleaned Missed Game dataframe
missed_games_events_df = pickle.load(open(mg_cleaned_pickle_path, "rb" )) 

#Read in previously scraped, cleaned, and processed schedule data
team_schedules_df = pickle.load(open(teams_schedule_pickle_path, "rb" )) 

#-----Feature Engineering - Section 1: Count Number of Missed Games--------

missed_games_events_df['Reg_games_missed'] = ''
missed_games_events_df['Post_games_missed'] = ''
missed_games_events_df['Season'] = ''
missed_games_events_df['Year'] = ''


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


#------------Feature Engineering - Section 2: Filter Notes --------------------
missed_games_events_df['note_keyword'] = ''
missed_games_events_df['category'] = ''

#apply notes_filter function to each row in dataframe
missed_games_events_df[['note_keyword', 'category']]= missed_games_events_df.apply(notes_filter, axis = 1, result_type="expand")

#-----------------------Save Data-----------------------------
#save file
pickle.dump(missed_games_events_df, open(savepath, "wb" ) )        
        