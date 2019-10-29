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
#player stats for 2017 and 2018 NBA seasons
player_stats_recent_df = player_stats_df[~player_stats_df['Year'].isin([2017,2018])]
player_stats_recent_df = player_stats_recent_df[['Age','TMP_prior_seasons']]

#create joint plot for showing distribution of age and career minutes for 2017 and 2018 NBA season
jointplot_ps_recent= sns.jointplot(data = player_stats_recent_df, x = "Age", y = "TMP_prior_seasons", kind='kde')

#format axis labels
jointplot_ps_recent.set_axis_labels('Age', 'Career Minutes', fontsize=16, weight = 'bold')

#save plot
jointplot_ps_recent.savefig('../../results/01_plots/distplot_players_recent.png')

#player stats for 2010 to 2016 NBA seasons
player_stats_older_df = player_stats_df[player_stats_df['Year'].isin([2017,2018])]
player_stats_older_df = player_stats_older_df[['Age','TMP_prior_seasons']]

jointplot_ps_older= sns.jointplot(data = player_stats_older_df, x = "Age", y = "TMP_prior_seasons", kind='kde', color = 'g')

#format axis labels
jointplot_ps_older.set_axis_labels('Age', 'Career Minutes', fontsize=16, weight = 'bold')

#save plot
jointplot_ps_older.savefig('../../results/01_plots/distplot_players_older.png')

#injuries for 2017 and 2018 seasons
injuries_recent_df = injury_df[injury_df['Year'].isin([2017,2018])]
injuries_recent_df = injuries_recent_df[['Age','TMP_prior_seasons']]
#
jointplot_inj_recent = sns.jointplot(data = injuries_recent_df, x = "Age", y = "TMP_prior_seasons", kind='kde', color = 'r')

#format axis labels
jointplot_inj_recent.set_axis_labels('Age', 'Career Minutes', fontsize=16, weight = 'bold')

#save plot
jointplot_inj_recent.savefig('../../results/01_plots/distplot_inj_recent.png')

#injureis for 2010-2016 NBA seasons
injuries_older_df = injury_df[~injury_df['Year'].isin([2017,2018])]
Injureis_older_df = injuries_older_df[['Age','TMP_prior_seasons']]
#
jointplot_inj_older = sns.jointplot(data = injuries_older_df, x = "Age", y = "TMP_prior_seasons", kind='kde', color = 'm')

#format axis labels
jointplot_inj_older.set_axis_labels('Age', 'Career Minutes', fontsize=16, weight = 'bold')

#save plot
jointplot_inj_older.savefig('../../results/01_plots/distplot_inj_older.png')

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