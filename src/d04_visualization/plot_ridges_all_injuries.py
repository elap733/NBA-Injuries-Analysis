# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 12:46:48 2019

@author: evanl
"""
from __future__ import unicode_literals
import joypy
from matplotlib import pyplot as plt
import pickle

#--------------------------User Inputs---------- ----------------------
#file path for pickle of concatenated/merged mg,il, player stats dataframes
injury_df_filepath =  '../../data/03_processed/mg_il_ps_merged_df.p'

#save path for plot
plot_savepath =  '../../results/01_plots/ridge_plot_all_injuries.png'

#-------------------------Load Files------------------------------------------
#load player injury event dataframe
injury_df = pickle.load(open(injury_df_filepath, "rb" ) )

#-------------------------Process Dataframe----------------------------------

#Add a column for total (regular + post season) games missed
injury_df['Tot_games_missed'] = injury_df['Reg_games_missed'] + injury_df['Post_games_missed']

"""Slice data set"""

#Only look at players that averaged more than 10 minutes per game ('MPPG' > 10)
injury_df = injury_df[injury_df['MPPG'] > 10.0]

#Exclude those 'injuries' which are not relevant (healthy scratches, rest, sick, n/a, other)
injury_df = injury_df[~ injury_df['category'].isin(['healthy inactive','rest','sick','other','n/a'])]

#Only look at serious injuries
injury_df = injury_df[injury_df['Tot_games_missed'] > 0]

#--------------------------Plot------------------------------------------------
injury_df = injury_df[injury_df['Season'].isin(['regular','post'])]
injury_df = injury_df[['Year','Game_number']]

fig, axes = joypy.joyplot(injury_df, by='Year', column='Game_number',hist = 'True', bins =25, overlap = 0, figsize=(5,8))

#Set axis labels
ax = axes[-1]
ax.set_xlabel("Game Number", fontsize = 18)
ax.set_title("Injury Events", fontsize = 20, weight = 'bold')

plt.show()
#----------------------Save plot---------------------------------------------
fig = ax.get_figure()
fig.savefig(plot_savepath, dpi = 150, bbox_extra_artists=(), bbox_inches='tight')