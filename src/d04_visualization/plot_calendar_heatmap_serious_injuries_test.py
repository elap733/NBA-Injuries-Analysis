# -*- coding: utf-8 -*-
"""
This script creates a heat map showing the number of days missed due to serious
injury by month and year. Technically this plot shows the number of games missed due
to injury events that occured in that month NOT the number of games missed that
month. For instance if a player tore his ACL in November and was out for the
rest of the season, all of those missed games would be assigned to November.

serious injury = injury causing a player to miss more than 15 games

Required:
    -mg_il_ps_merged_df.p
    
Outputs:
    -stacked bar chart


@author: evanl
"""
import seaborn as sns
from matplotlib import pyplot as plt
import pickle

#--------------------------User Inputs---------- ----------------------
#file path for pickle of concatenated/merged mg,il, player stats dataframes
injury_df_filepath =  '../../data/03_processed/mg_il_ps_merged_df.p'


#save path for plot
plot_savepath =  '../../results/01_plots/calendar_heat_map_serious_injury.png'

#-------------------------Load Files------------------------------------------

#load player injury event dataframe
injury_df = pickle.load(open(injury_df_filepath, "rb" ) )

#-------------------------Process Injury DataFrame---------------------------

#Add a column for total (regular + post season) games missed
injury_df['Tot_games_missed'] = injury_df['Reg_games_missed'] + injury_df['Post_games_missed']

#Extract month from datetime64
injury_df['Month'] = injury_df['Date'].dt.month

month_dictionary= {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October', 
        11: 'November',
        12: 'December'}

#Convert month from a numeric (1-12) to text using month_dictionary
injury_df['Month'] = injury_df['Month'].map(month_dictionary )

#Only look at players that averaged more than 10 minutes per game ('MPPG' > 10)
injury_df = injury_df[injury_df['MPPG'] > 10.0]

#Exclude those 'injuries' which are not relevant (healthy scratches, rest, sick, n/a, other)
injury_df = injury_df[~ injury_df['category'].isin(['healthy inactive','rest','sick','other','n/a'])]

##Only look at serious injuries
injury_df = injury_df[injury_df['Tot_games_missed'] >= 15]

#Only look at 2010-2018
injury_df = injury_df[injury_df['Year'] != 2009]

#Groupby year and month, sum total games missed, then unstack for plotting
grouped_df = injury_df.groupby(['Year','Month'])['Tot_games_missed'].sum().unstack()

#Fill NaN with zeros
grouped_df = grouped_df.fillna(0)

##Add back in April for plotting clarity
grouped_df['April'] = 0

#Reorder months to match season start --> finish 
grouped_df = grouped_df[['October','November', 'December', 'January', 'February','March', 'April', 'May']]

#--------------------------Plot------------------------------------------------

fig = plt.figure(figsize=(12,12))
r = sns.heatmap(grouped_df, cmap='Reds')
r.set_title("Heatmap of Games Missed Due to Serious Injury", fontsize = 20, weight = 'bold')
r.set_ylabel('Year', fontsize = 16, weight = 'bold')
r.set_xlabel('Month', fontsize = 16, weight = 'bold')


##----------------------Save plot---------------------------------------------
fig = r.get_figure()
fig.savefig(plot_savepath)