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

#file path for pickle of player stats dataframe with feature engineering
player_stats_df_filepath =  '../../data/03_processed/player_stats_processed.p'

#save path for plot
plot_savepath =  '../../results/01_plots/distplot_injury_durations.png'

#-------------------------Load Files------------------------------------------
#load player injury event dataframe
injury_df = pickle.load(open(injury_df_filepath, "rb" ) )



#-------------------------Process Injury DataFrame---------------------------

#Add a column for total (regular + post season) games missed
injury_df['Tot_games_missed'] = injury_df['Reg_games_missed'] + injury_df['Post_games_missed']

"""Slice data set"""

#Only look at players that averaged more than 10 minutes per game ('MPPG' > 10)
injury_df = injury_df[injury_df['MPPG'] > 10.0]

#Exclude those 'injuries' which are not relevant (healthy scratches, rest, sick, n/a, other)
injury_df = injury_df[~ injury_df['category'].isin(['healthy inactive','rest','sick','other','n/a'])]

#Only look at serious injuries
injury_df = injury_df[injury_df['Tot_games_missed'] >= 15]


#--------------------------Plot------------------------------------------------
last_two_years_df = injury_df[injury_df['Year'].isin([2013])]
other_years_df = injury_df[injury_df['Year'].isin([2017])]
fig, ax = plt.subplots()
sns.distplot(last_two_years_df['Game_number'], kde = False, ax = ax, bins = 82)
sns.distplot(other_years_df['Game_number'],kde = False, ax = ax, bins = 82)
ax.set_xlabel(xlabel ='Game Number', fontsize = 16, weight = 'bold')
ax.set_xticklabels(ax.get_xticks(), fontsize = 16)
ax.set_yticklabels(ax.get_yticks(), fontsize =16)
ax.legend(labels=[ '2013', '2017'], fontsize =14, loc='best')
#sns.plt.show()




last_two_years_df = injury_df[injury_df['Year'].isin([2016])]
other_years_df = injury_df[injury_df['Year'].isin([2018])]
fig, ax = plt.subplots()
sns.distplot(last_two_years_df['Tot_games_missed'], kde = False, ax = ax, bins = 25)
sns.distplot(other_years_df['Tot_games_missed'],kde = False, ax = ax, bins = 25)
ax.set_xlabel(xlabel ='Injury Duration (Days)', fontsize = 16, weight = 'bold')
ax.set_xticklabels(ax.get_xticks(), fontsize = 16)
ax.set_yticklabels(ax.get_yticks(), fontsize =16)
ax.legend(labels=[ '2016', '2018'], fontsize =14, loc='best')
#sns.plt.show()
#

last_two_years_df = injury_df[~injury_df['Year'].isin([2017,2018])]
other_years_df = injury_df[injury_df['Year'].isin([2017,2018])]
fig, ax = plt.subplots()
sns.distplot(last_two_years_df['Tot_games_missed'], hist = False, kde_kws={"shade": True}, ax = ax)
sns.distplot(other_years_df['Tot_games_missed'],hist = False, kde_kws={"shade": True}, ax = ax)
ax.set_xlabel(xlabel ='Injury Duration (Days)', fontsize = 16, weight = 'bold')
ax.set_xticklabels(ax.get_xticks(), fontsize = 16)
ax.set_yticklabels(ax.get_yticks(), fontsize =16)
ax.legend(labels=[ '2010-2016', '2017-2018'], fontsize =14, loc='best')
sns.plt.show()
##----------------------Save plot---------------------------------------------
fig = ax.get_figure()
fig.savefig(plot_savepath)