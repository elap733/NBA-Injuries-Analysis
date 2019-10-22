# -*- coding: utf-8 -*-
"""
This script creates a correlation matrix plot that includes:
    - Total games missed due to an injury
    - Age at time of injury
    - Total minutes played prior seasons

@author: evanl
"""

from matplotlib import pyplot as plt
import pickle
import pandas as pd
#--------------------------User Inputs---------- ----------------------
#file path for pickle of concatenated/merged mg,il, player stats dataframes
injury_df_filepath =  '../../data/03_processed/mg_il_ps_merged_df.p'

#save path for plot
plot_savepath =  '../../results/01_plots/correlation_plots.png'

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
injury_df = injury_df[['Tot_games_missed', 'Age', 'TMP_prior_seasons']]
injury_df.rename(columns = {'Tot_games_missed': 'Injury Duration', 'Age': 'Age', 'TMP_prior_seasons': 'Minutes Played'}, inplace = True)
sm = pd.plotting.scatter_matrix(injury_df, figsize=(10, 10))

for ax in sm.ravel():
    ax.set_xlabel(ax.get_xlabel(), fontsize = 18)
    ax.set_ylabel(ax.get_ylabel(), fontsize = 18)
    
plt.show()

plt.savefig(plot_savepath)
#----------------------Save plot---------------------------------------------
#fig = ax.get_figure()
#fig.savefig(plot_savepath, dpi = 150, bbox_extra_artists=(), bbox_inches='tight')