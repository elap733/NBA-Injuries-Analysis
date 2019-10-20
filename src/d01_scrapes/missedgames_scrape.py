# -*- coding: utf-8 -*-
"""
This script scrapes the website www.prosportstransactions.com for NBA missed 
game data and builds a data frame using that data. Each row in the data frame
corresponds to a missed game "event" for a player. The columns are:
date (of event), player's team, name of player inactivated,
name of player reactivated, additional notes. This data frame is then saved as
a .csv file for later use.
  
@author: evanl
"""
#import packages for scraping
import os
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

#------- User Inputs -----------------------
#save path and output filename
savepath='C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/Missed Games'
filename = 'prosportstransactions_scrape_missedgames_2010_2019.csv'

#URL to scrape from 
url = "https://www.prosportstransactions.com/basketball/Search/SearchResults.php?Player=&Team=&BeginDate=2010-08-01&EndDate=2019-08-27&InjuriesChkBx=yes&PersonalChkBx=yes&Submit=Search"
#Note that only the first subset of results is shown on this webpage. The remainder of the data is broken out into a number of web pages that are linked at the bottom. 


#-------------Scrape web page--------------------------------------

#Get URL HTML
response = requests.get(url)
print(response) # Response [200] means it went through

#Parse HTML with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

#-------------Scrape data from the first web page----------------
#Read in html as pandas data frame
df_first_page = pd.read_html(url)
    
#Select table of interest (the first table)
df_first_page = df_first_page[0]

#Drop first row (column names)
df_first_page.drop([0], inplace = True)
   
#Remove bullet in front of player names
df_first_page[2]=df_first_page[2].str[2:] # "Acquired" column
df_first_page[3]=df_first_page[3].str[2:] # "Relinquished" column
    
#Modify column titles
df_first_page.columns = ['Date','Team','Acquired','Relinquished','Notes']

#data frame to hold data
appended_data = df_first_page

#------------Scrape data from other pages linked at the bottom of the first page------------
# Loop over links (skipping the first 4 (not data) and last 4 ("Next" and other webpage links))
for i in range(4,len(soup.findAll('a'))-4): #'a' tags are for links
   
    #find all links on webpage and select the i-th link
    one_a_tag = soup.findAll('a')[i]
    link = one_a_tag['href']
    
    #Add in the rest of the url
    download_url = 'https://www.prosportstransactions.com/basketball/Search/'+ link
    print(download_url)
    
    #Read html as pandas data frame
    dfs = pd.read_html(download_url)
    
    #Select table of interest (the first table)
    df = dfs[0]
    
    #Drop first row (column names)
    df.drop([0], inplace = True)
   
    #Remove bullet in front of names
    df[2]=df[2].str[2:] # "Acquired" column
    df[3]=df[3].str[2:] # "Relinquished" column
    
    #Modify column titles
    df.columns = ['Date','Team','Acquired','Relinquished','Notes']
    
    #Append data frame 
    appended_data=pd.concat([appended_data,df], ignore_index=True)
    
    #Add a pause to keep web server happy
    time.sleep(3)
    
print(appended_data.shape)

#save file
filename= os.path.join(savepath,filename)
appended_data.to_csv(filename)
