# -*- coding: utf-8 -*-
"""

@author: evanl
"""
import seaborn as sns
from matplotlib import pyplot as plt
import pickle

#--------------------------User Inputs---------- ----------------------
#file path for pickle of concatenated/merged mg,il, player stats dataframes
injury_df_filepath =  '../../data/03_processed/mg_il_ps_merged_df.p'


#save path for plot
plot_savepath =  '../../results/01_plots/calendar_plots.png'

#-------------------------Load Files------------------------------------------
#load player injury event dataframe
injury_df = pickle.load(open(injury_df_filepath, "rb" ) )


#-------------------------Process Injury DataFrame---------------------------

#Add a column for total (regular + post season) games missed
injury_df['Tot_games_missed'] = injury_df['Reg_games_missed'] + injury_df['Post_games_missed']

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

injury_df['Month'] = injury_df['Month'].map(month_dictionary )

#Only look at players that averaged more than 10 minutes per game ('MPPG' > 10)
injury_df = injury_df[injury_df['MPPG'] > 10.0]

#Exclude those 'injuries' which are not relevant (healthy scratches, rest, sick, n/a, other)
injury_df = injury_df[~ injury_df['category'].isin(['healthy inactive','rest','sick','other','n/a'])]

#Only look at serious injuries
injury_df = injury_df[injury_df['Tot_games_missed'] >= 15]

injury_df = injury_df[injury_df['Year'] != 2009]

grouped_df = injury_df.groupby(['Year','Month'])['Tot_games_missed'].sum().unstack()

grouped_df = grouped_df.fillna(0)

grouped_df['April'] = 0

grouped_df = grouped_df[['October','November', 'December', 'January', 'February','March', 'April', 'May']]

fig = plt.figure(figsize=(12,12))
r = sns.heatmap(grouped_df, cmap='Reds')
r.set_title("Heatmap of Games Missed 2010-2018")



#--------------------------Plot------------------------------------------------

##----------------------Save plot---------------------------------------------
fig = ax.get_figure()
fig.savefig(plot_savepath)