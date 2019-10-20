# -*- coding: utf-8 -*-
"""
This script scrapes, cleans, and processes www.basketball-reference.com 
for historical NBA team schedules. 

- Cleaning and processing
    - Team name
    - Date formating
    - Game number
    - Season year column
    - Season type (regular or post) column

Outputs:
    -.csv files for each NBA team; each file contains schedule "data" for
    multiple seasons for that team. 
    - a 'master schedule' .csv file and pickle dataframe that has the schedule
    "data" for  all teams. 

Each row corresponds to a game; columns indicate team name, season, 
game number, game date, an indicator (flag) for home/away, opponent, and an 
indicator for whether a game went into overtime (OT).

@author: evanl
"""
#import packages for scraping
import os
import pandas as pd
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle

#--------------------------User Inputs -----------------------
#save path for csv files
savepath_csv='C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/Schedules'

#save path and output filename for pickle
savepath_pickle='C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/Schedules/all_teams_schedule_2010_2020.p'


#seasons schedules to scrape
season_list = ['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']

#NBA teams to scrape (this dictionary is valid (complete) for 2009-2019 seasons)
team_dict = {
    'ATL': 'Atlanta Hawks',
    'BOS': 'Boston Celtics',
    'BRK': 'Brooklyn Nets',
    'CHA': 'Charlotte Bobcats',
    'CHI': 'Chicago Bulls',
    'CHO': 'Charlotte Hornets',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LAC': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NJN': 'New Jersey Nets',
    'NOH': 'New Orleans Hornets',
    'NOP': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHO': 'Phoenix Suns',
    'POR': 'Portland Trailblazers',
    'SAC': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'WAS': 'Washington Wizards'   
}

#teams that moved or otherwise had a name change - need to handle these teams separately (this dictionary is valid for 2009-2019)
teams_relocate_rename_dict = {
    'BRK': ['2013', '2014', '2015', '2016', '2017', '2018', '2019','2020'],
    'CHA': ['2010', '2011', '2012', '2013','2014'],
    'CHO': ['2015', '2016', '2017', '2018', '2019','2020'],
    'NJN': ['2010', '2011', '2012'],
    'NOH': ['2010','2011','2012','2013'],
    'NOP': ['2014', '2015', '2016', '2017', '2018', '2019','2020'],
}
#---------------------Define Functions-----------------------

def sched_scrape_clean_process(team_abrv,year,team_dict):
    
    """
    This function scrapes season schedules. It has three inputs: team_abrv (a string; i.e. 'POR'),a year (a string; i.e. '2017'),
    and a dictionary containing team names; Output is a dataframe with schedule information.
    """
    #website URL to scrape 
    url = "https://www.basketball-reference.com/teams/{}/{}_games.html". format(team_abrv,year)
    html = urlopen(url)
    
    soup = BeautifulSoup(html,features="lxml")

    # use findALL() to get the column headers
    soup.findAll('tr', limit=1)

    #find all rows in table
    rows = soup.findAll('tr')
    sched_data = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

    #create a panda frame 
    sched_df = pd.DataFrame(sched_data)

    #drop columns that aren't needed (keeping date, home/away, opponent, OT info)
    sched_df.drop(columns = [1,2,3,6,8,9,10,11,12,13], inplace = True)

    #add column headers
    sched_df.columns = ['Date','Away_flag','Opponent','OT_flag']

    #drop empty rows (empty rows exist due to table formatting, not missing data)
    sched_df.dropna(subset = ['Date'], inplace = True)

    #add a column indicating the game number for a given season
    sched_df.reset_index(inplace = True)
    sched_df['Game_num'] = sched_df.index + 1

    #add a column indicating the team
    sched_df['Team'] = team_dict[team_abrv]

    #add a column indicating the year in which the season begins
    sched_df['Year'] = str(int(year) - 1)
    
    #add a column indicating the season (regular, post)
    season_holder = []
    for row in sched_df.itertuples():
        if row.Year != '2011':
            if row.Game_num <= 82:
                season_holder.append('regular')
            else: 
                season_holder.append('post')
        else:
            if row.Game_num <= 66:
                season_holder.append('regular')
            else: 
                season_holder.append('post')
                
    sched_df['Season'] = season_holder
    
    #reorder columns
    sched_df = sched_df[['Team','Year', 'Season', 'Game_num','Date','Away_flag','Opponent','OT_flag']]

    #convert 'Date' to datetime format
    sched_df['Date']=pd.to_datetime(sched_df['Date'],format='%a, %b %d, %Y', errors = 'coerce')
    sched_df['Date']=pd.to_datetime(sched_df['Date'],infer_datetime_format=True)
    
    #modify "Away_flag" column; "@" = 1, null = 0
    sched_df['Away_flag']=sched_df['Away_flag'].map({'@':1,'': 0})

    return sched_df

#------------------------Scrape and Clean ------------------------------
#create an empty data frame to hold the schedules for all teams, all seasons 
all_teams_sched_df = pd.DataFrame()

"""
The loop below scrapes schedule data. 
- Loops over team and loops over year. 
- Saves each team's schedule data (multiple seasons)as a separate csv file
(one .csv file per team)
"""
for team in team_dict:
    
    team_sched_df = pd.DataFrame(columns = ['Team','Year','Season','Game_num','Date','Away_flag','Opponent','OT_flag']) #create empty dataframe with column headers
    
    if team not in teams_relocate_rename_dict: #for those teams that didn't (a) change cities, or (b) otherwise have a name change
        for year in season_list:
            single_season_df = sched_scrape_clean_process(team, year,team_dict)
            team_sched_df=pd.concat([team_sched_df,single_season_df], ignore_index=True)
            print('Scraped {} {} game schedule'.format(team,year))
            #Add a pause to keep web server happy
            time.sleep(7)
       
        print('Saving multi-season schedule to .csv - {} game schedule {} - {}'.format(team, season_list[0], season_list[-1]))
        #save file
        filename = '{}_schedule_{}_{}.csv'.format(team, season_list[0], season_list[-1])
        filename= os.path.join(savepath_csv,filename)
        team_sched_df.to_csv(filename)
    else:    
        for year in teams_relocate_rename_dict[team]: #for those team that either moved or otherwise had a name change
            single_season_df = sched_scrape_clean_process(team, year,team_dict)
            team_sched_df=pd.concat([team_sched_df,single_season_df], ignore_index=True)
            print('Scraped {} {} game schedule'.format(team,year))
            #Add a pause to keep web server happy
            time.sleep(7)
        
        print('Saving multi-season schedule to .csv - {} game schedule {} - {}'.format(team, season_list[0], season_list[-1]))
        #save file
        filename = '{}_schedule_{}_{}.csv'.format(team, season_list[0], season_list[-1])
        filename= os.path.join(savepath_csv,filename)
        team_sched_df.to_csv(filename)
    
    #append 'master schedule' data frame with team's schedule
    all_teams_sched_df = pd.concat([all_teams_sched_df, team_sched_df], ignore_index=True)   

#-------------------------Save master schedule-----------------------------
#save 'master schedule' file as csv
filename = 'all_teams_schedule_{}_{}.csv'.format(season_list[0], season_list[-1])
filename= os.path.join(savepath_csv,filename)
all_teams_sched_df.to_csv(filename)

#save 'master schedule' file as csv and pickle
pickle.dump(all_teams_sched_df, open(savepath_pickle, "wb" ) )