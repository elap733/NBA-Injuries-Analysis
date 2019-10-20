# -*- coding: utf-8 -*-
"""
This script scrapes www.basketball-reference.com for historical NBA player 
stats over a user-defined season range. It scrapes both regular season and playoff
stats. It outputs a .csv file. Each row corresponds to a player' stats in a
given season. Stats are "per game" totals for a given season.

@author: evanl
"""

#import packages for scraping
import os
import pandas as pd
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup

### -------------------------User Inputs ------------------------------------
#save path and output filename
savepath='../../data/01_raw/'

# NBA seasons we will be analyzing
year_list = list(range(1994,2020))

#--------------------------Define Functions----------------------------------

def stats_scrape(year, season_type):
    
    """
    This function scrapes season stats. It has two inputs: year (an integer; i.e. 2017); 
    and season_type(a string; which is either 'regular' or 'post'). Output is a 
    dataframe with stats.
    """
    if season_type == 'regular':
        url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
    elif season_type == 'post':
        url = "https://www.basketball-reference.com/playoffs/NBA_{}_per_game.html".format(year)
        
    html = urlopen(url)
    soup = BeautifulSoup(html,features="lxml")

    # use findALL() to get the column headers
    soup.findAll('tr', limit=1)
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=1)[0].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]

    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    #scrape data from each row
    player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
    
    #create a pandas dataframe from scraped data
    player_stats_df = pd.DataFrame(player_stats, columns = headers)
    
    #drop empty rows (empty rows exist due to table formatting, not missing data)
    player_stats_df.dropna(subset = ['Player'], inplace = True)
    
    #add a column to indicate year
    player_stats_df.insert(0, "Year", [year - 1]*(len(player_stats_df.index)))
    
    #add a column to indicate if stats are for regular season or playoffs
    player_stats_df.insert(1, "Season", [season_type]*(len(player_stats_df.index)))
    
    return player_stats_df

#--------------------------Scrape Data----------------------------------------
  
#create empty data frame to hold player stats
all_player_stats_df = pd.DataFrame()

#loop over season of interests and scrape regular and playoff stats
for year in year_list:
    reg_season_df = stats_scrape(year, 'regular')
    all_player_stats_df=pd.concat([all_player_stats_df,reg_season_df], ignore_index=True)
    post_season_df = stats_scrape(year, 'post')
    all_player_stats_df=pd.concat([all_player_stats_df,post_season_df], ignore_index=True)
    
    print('Scraped {} regular and post season player stats'.format(year))
    #Add a pause to keep web server happy
    time.sleep(7)
    

#save dataframe as  a csv file       
print('Saving multi-season player stats data to .csv - seasons {} - {}'.format(year_list[0], year_list[-1]))
filename = 'player_stats_{}_{}.csv'.format(year_list[0], year_list[-1])
filename= os.path.join(savepath,filename)
all_player_stats_df.to_csv(filename)
    