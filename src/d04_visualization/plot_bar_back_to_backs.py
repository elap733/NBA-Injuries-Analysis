# -*- coding: utf-8 -*-
"""
This script creates a bar chart displaying the number of back-to-back sets
played each season. A "back-to-back" set is defined as two games played on
consecutive calendar days.

Required inputs:
    -all_teams_schedule_2010_2020_processed.p
    
Outputs:
    -bar chart
    
@author: evanl
"""
import numpy as np
import pandas as pd
import pickle

pd.set_option('display.expand_frame_repr', False)

#--------------------------User Inputs---------- ----------------------
#file path for pickle of processed schedule dataframes
schedule_df_filepath =  '../../data/03_processed/all_teams_schedule_2010_2020_processed.p'

#save path for plot
plot_savepath =  '../../results/01_plots/bar_back_to_backs.png'

#-------------------------Load Files------------------------------------------
#load schedules dataframe
schedule_df = pickle.load(open(schedule_df_filepath, "rb" ) )

#-------------------------Process Dataframe----------------------------------

#calculate the number of calendar days between each game
schedule_df['date_diff']=schedule_df['Date'].diff() / np.timedelta64(1, 'D')
back_to_backs_df = schedule_df[schedule_df['date_diff'] == 1]

#restrict to years 2010-2018
back_to_backs_df = back_to_backs_df[~back_to_backs_df['Year'].isin([2009,2019])]

#restrict to regular season games
back_to_backs_df = back_to_backs_df[back_to_backs_df['Season'] == 'regular']
#------------------------Make plots-------------------------------------------

#group by year and count the number of back-to-backs
data = back_to_backs_df.groupby(['Year']).count()


#create plot
ax = data['Date'].plot(kind='bar',  figsize=(15, 10), color = ['dimgray', 'dimgray', 'dimgray', 'dimgray', 'dimgray', 'dimgray', 'dimgray', 'dimgray', 'red'])

# Set the x-axis label
ax.set_xlabel("Year", fontsize = 16, weight='bold')

# Set the y-axis label
ax.set_ylabel("Count of Back-to-Backs", fontsize =16,weight='bold')

# Set the x-axis tick labels
ax.set_xticklabels(data.index,rotation = 0, fontsize = 16)

# Set the y-axis tick labels
y_tick_labels = []
for tick in ax.get_yticks():
    y_tick_labels.append(int(tick))
    
ax.set_yticklabels(y_tick_labels, fontsize = 16)

#plot title
ax.set_title('Back-to-Back Game Sets', fontsize = 24, weight= 'bold')


#----------------------Save plot---------------------------------------------
fig = ax.get_figure()
fig.savefig(plot_savepath, dpi = 300)