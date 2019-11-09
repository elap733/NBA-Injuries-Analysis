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

#save paths for plots
plot_savepath_age_all =  '../../results/01_plots/distplot_age_all.png'
plot_savepath_minutes_all =  '../../results/01_plots/distplot_min_all.png'
plot_savepath_age_injured =  '../../results/01_plots/distplot_age_inj.png'
plot_savepath_minutes_injured =  '../../results/01_plots/distplot_min_inj.png'

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

#player stats for 2017 and 2018 NBA seasons
player_stats_recent_df = player_stats_df[~player_stats_df['Year'].isin([2017,2018])]

#age and minutes played for all players with >10 MPPG, 2017-2018 NBA seasons
player_stats_recent_df = player_stats_recent_df[['Age','TMP_prior_seasons']]

#player stats for 2010 to 2016 NBA seasons
player_stats_older_df = player_stats_df[player_stats_df['Year'].isin([2017,2018])]

#age and minutes played for all players with >10 MPPG, 2010-2016 NBA seasons
player_stats_older_df = player_stats_older_df[['Age','TMP_prior_seasons']]

##injuries for 2017 and 2018 seasons
injuries_recent_df = injury_df[injury_df['Year'].isin([2017,2018])]

#age and minutes played for injured players with >10 MPPG, 2017-2018 NBA seasons
injuries_recent_df = injuries_recent_df[['Age','TMP_prior_seasons']]

#injuries for 2010 to 2016 NBA seasons
injuries_older_df = injury_df[~injury_df['Year'].isin([2017,2018])]

#age and minutes played for injured players with >10 MPPG, 2010-2016 NBA seasons
injuries_older_df = injuries_older_df[['Age','TMP_prior_seasons']]


#-------------Create "All Players" Age and Minutes played plots----------------
#Create dist plot comparing player age distributions 
fig, ax = plt.subplots()
             
sns.distplot(player_stats_older_df['Age'].values,color ='b', hist = False, kde_kws={"shade": True}, ax = ax)

sns.distplot(player_stats_recent_df['Age'].values,color ='r', hist = False, kde_kws={"shade": True}, ax = ax)

ax.set(xlim = (14,50))
ax.set_xlabel(xlabel ='Age', fontsize = 16, weight = 'bold')
xlabels = [str(int(x)) for x in ax.get_xticks()]
ax.set_xticklabels(xlabels, fontsize = 16)
ax.set_yticklabels(ax.get_yticks(), fontsize =16)
ax.legend(labels=[ '2010-2016 seasons', '2017-2018 seasons'], fontsize =14, loc='best')
title = ax.set_title(label = 'All Players (>10 MPPG)',fontsize=15,weight ='bold', )   

#Save plot
fig = ax.get_figure()
fig.savefig(plot_savepath_age_all, dpi = 300, bbox_extra_artists=(), bbox_inches='tight')

#Create dist plot comparing distribution of cummulative minutes played in prior seasons
fig, ax = plt.subplots()
             
sns.distplot(player_stats_older_df['TMP_prior_seasons'].values,color ='b', hist = False, kde_kws={"shade": True}, ax = ax)

sns.distplot(player_stats_recent_df['TMP_prior_seasons'].values,color ='r', hist = False, kde_kws={"shade": True}, ax = ax)

ax.set_xlabel(xlabel ='Career Minutes Played Entering Season', fontsize = 16, weight = 'bold')
xlabels = [str(int(x)) + 'K' for x in ax.get_xticks()/1000]
ax.set_xticklabels(xlabels, fontsize = 16)
ylabels = ['{0:.1E}'.format(y) for y in ax.get_yticks()]
ax.set_yticklabels(ylabels, fontsize =16)
ax.legend(labels=[ '2010-2016 seasons', '2017-2018 seasons'], fontsize =14, loc='best')
title = ax.set_title(label = 'All Players (>10 MPPG)',fontsize=15,weight ='bold', )   

#Save plot
fig = ax.get_figure()
fig.savefig(plot_savepath_minutes_all, dpi = 300, bbox_extra_artists=(), bbox_inches='tight')

#-------------Create "Injured Players" Age and Minutes played plots----------------
#Create dist plot comparing player age distributions 
fig, ax = plt.subplots()
             
sns.distplot(injuries_older_df['Age'].values,color ='b', hist = False, kde_kws={"shade": True}, ax = ax)

sns.distplot(injuries_recent_df['Age'].values,color ='r', hist = False, kde_kws={"shade": True}, ax = ax)

ax.set(xlim = (14,50))
ax.set_xlabel(xlabel ='Age', fontsize = 16, weight = 'bold')
xlabels = [str(int(x)) for x in ax.get_xticks()]
ax.set_xticklabels(xlabels, fontsize = 16)
ax.set_yticklabels(ax.get_yticks(), fontsize =16)
ax.legend(labels=[ '2010-2016 seasons', '2017-2018 seasons'], fontsize =14, loc='best')
title = ax.set_title(label = 'Injured Players (>10 MPPG)',fontsize=15,weight ='bold', )   

#Save plot
fig = ax.get_figure()
fig.savefig(plot_savepath_age_injured, dpi = 300, bbox_extra_artists=(), bbox_inches='tight')

#Create dist plot comparing distribution of cummulative minutes played in prior seasons
fig, ax = plt.subplots()
             
sns.distplot(injuries_older_df['TMP_prior_seasons'].values,color ='b', hist = False, kde_kws={"shade": True}, ax = ax)

sns.distplot(injuries_recent_df['TMP_prior_seasons'].values,color ='r', hist = False, kde_kws={"shade": True}, ax = ax)

ax.set_xlabel(xlabel ='Career Minutes Played Entering Season', fontsize = 16, weight = 'bold')
xlabels = [str(int(x)) + 'K' for x in ax.get_xticks()/1000]
ax.set_xticklabels(xlabels, fontsize = 16)
ylabels = ['{0:.1E}'.format(y) for y in ax.get_yticks()]
ax.set_yticklabels(ylabels, fontsize =16)
ax.legend(labels=[ '2010-2016 seasons', '2017-2018 seasons'], fontsize =14, loc='best')
title = ax.set_title(label = 'Injured Players (>10 MPPG)',fontsize=15,weight ='bold', )   

#Save plot
fig = ax.get_figure()
fig.savefig(plot_savepath_minutes_injured,dpi = 300, bbox_extra_artists=(), bbox_inches='tight')
