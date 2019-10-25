# -*- coding: utf-8 -*-
"""
This script creates a distribution plot of age for all NBA players averaging 10 
minutes per game or more a season 2010-2018, and for injured NBA players during
the same seasons.


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
plot_savepath =  '../../results/01_plots/distplot_age.png'

#-------------------------Load Files------------------------------------------
#load player injury event dataframe
injury_df = pickle.load(open(injury_df_filepath, "rb" ) )


#load player player stats dataframe
player_stats_df = pickle.load(open(player_stats_df_filepath, "rb" ) )


#-------------------------Process Injury DataFrame---------------------------

#Add a column for total (regular + post season) games missed
injury_df['Tot_games_missed'] = injury_df['Reg_games_missed'] + injury_df['Post_games_missed']

"""Slice data set"""

#Only look at players that averaged more than 10 minutes per game ('MPPG' > 10)
injury_df = injury_df[injury_df['MPPG'] > 10.0]

#Exclude those 'injuries' which are not relevant (healthy scratches, rest, sick, n/a, other)
injury_df = injury_df[~ injury_df['category'].isin(['healthy inactive','rest','sick','other','n/a'])]

#Only look at serious injuries
injury_df = injury_df[injury_df['Tot_games_missed'] > 0]

#-------------------------Process Player Stats DataFrame---------------------------


#Only look at players that averaged more than 10 minutes per game ('MPPG' > 10)
player_stats_df = player_stats_df[player_stats_df['MPPG'] > 10.0]

#Only keep players 2010-2019 seasons
player_stats_df = player_stats_df[player_stats_df['Year']> 2009]
#--------------------------Plots------------------------------------------------
data = player_stats_df[~player_stats_df['Year'].isin([2017,2018])]
data = data[['Age','TMP_prior_seasons']]

vis1 = sns.jointplot(data = data, x = "Age", y = "TMP_prior_seasons", kind='kde')

data = player_stats_df[player_stats_df['Year'].isin([2017,2018])]
data = data[['Age','TMP_prior_seasons']]

vis2 = sns.jointplot(data = data, x = "Age", y = "TMP_prior_seasons", kind='kde', color = 'g')

data = injury_df[~injury_df['Year'].isin([2017,2018])]
data = data[['Age','TMP_prior_seasons']]

vis1 = sns.jointplot(data = data, x = "Age", y = "TMP_prior_seasons", kind='kde', color = 'r')

data = injury_df[injury_df['Year'].isin([2017,2018])]
data = data[['Age','TMP_prior_seasons']]

vis2 = sns.jointplot(data = data, x = "Age", y = "TMP_prior_seasons", kind='kde', color = 'm')


#fig, ax = plt.subplots()
#sns.distplot(player_stats_df['Age'], hist = False, kde_kws={"shade": True}, ax = ax)
#sns.distplot(injury_df['Age'],hist = False, kde_kws={"shade": True}, ax = ax)
#ax.set_xlabel(xlabel ='Age', fontsize = 16, weight = 'bold')
#ax.set_xticklabels(ax.get_xticks(), fontsize = 16)
#ax.set_yticklabels(ax.get_yticks(), fontsize =16)
#ax.legend(labels=[ 'All NBA Players','Injured Players'], fontsize =14, loc='best')
#sns.plt.show()
#
##----------------------Save plot---------------------------------------------
fig = ax.get_figure()
fig.savefig(plot_savepath)