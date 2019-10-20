# -*- coding: utf-8 -*-
"""
    This function finds the nearest scheduled NBA game to a missed game (MG)/
    inactive list (IL) event. In many cases the event date corresponds exactly
    with a scheduled game (this almost always the case for MG events). In cases
    where it does not however, we must find the first game that occurs after 
    the event. 
    
    This function has three inputs:
        
    -'team_schedules_df' - scraped and cleaned schedule data
    - 'event_date'- date of MG or IL event
    - 'event_team'- the affected player's team
    
    Output is: 
    -- the game number closest to the MG/IL event 
    -- the season ('regular', 'post', 'off') during which the event occured
    -- the year in which the event occured 
    -- the number of post season games that team played in that year
"""
from datetime import timedelta

def correlate_event_to_game_schedule (team_schedules_df, event_date, event_team): 
  
    
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