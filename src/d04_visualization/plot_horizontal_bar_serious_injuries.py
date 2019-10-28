# -*- coding: utf-8 -*-
"""
This script creates a horizontal bar chart of missed games due to serious injury. Each 
bar represents an injured body part.

serious injury = an injury that causes a player to miss 15 or more games

Required inputs:
    -mg_il_ps_merged_df.p
    
Outputs:
    -stacked bar chart
    
@author: evanl
"""

import pandas as pd
import pickle


pd.set_option('display.expand_frame_repr', False)

#--------------------------User Inputs---------- ----------------------
#file path for pickle of concatenated/merged mg,il, player stats dataframes
injury_df_filepath =  '../../data/03_processed/mg_il_ps_merged_df.p'

#year to plot
year = 2018

#save path for plot
plot_savepath =  '../../results/01_plots/hor_bar_serious_injuries{}.png'.format(year)

#-------------------------Load Files------------------------------------------
#load player injury event dataframe
injury_df = pickle.load(open(injury_df_filepath, "rb" ) )

#-------------------------Process Dataframe----------------------------------

#Add a column for total (regular + post season) games missed
injury_df['Tot_games_missed'] = injury_df['Reg_games_missed'] + injury_df['Post_games_missed']

"""Slice data set"""

#Only look at players that averaged more than 10 minutes per game ('MPPG' > 10)
injury_df = injury_df[injury_df['MPPG'] > 10.0]

#Only look at serious injuries
injury_df = injury_df[injury_df['Tot_games_missed'] > 15]

#Exclude those 'injuries' which are not relevant (healthy scratches, rest, sick, n/a, other)
injury_df = injury_df[~ injury_df['category'].isin(['healthy inactive','rest','sick','other','n/a'])]

injury_df = injury_df[injury_df['Year'] == 2018]

#dictionary to simplify plot (plot fewer body parts by combining some - e.g. eye, nose = face)
injury_dictionary = {
        'foot': 'foot',
        'toe': 'toe',
        'heel': 'heel',
        'ankle': 'ankle',
        'achilles': 'achilles',
        'calf': 'calf',
        'shin': 'shin',
        'tibia': 'shin',
        'fibula': 'shin',
        'acl': 'knee',
        'mcl': 'knee',
        'knee': 'knee',
        'hamstring': 'hamstring',
        'quad': 'quad',
        'groin':'groin',
        'hip': 'hip',
        'femur':'quad',
        'shoulder':'shoulder',
        'back': 'torso',
        'torso':'torso',
        'ribs':'torso',
        'abdominal':'abdominal',
        'neck': 'head',
        'eye': 'face',
        'nose': 'face',
        'head': 'head',
        'finger':'finger',
        'hand':'hand',
        'arm': 'arm',
        'bicep':'arm',
        'tricep':'arm',
        'elbow': 'elbow',
        'wrist': 'wrist'
        }

#Map injury dictionary
injury_df['note_keyword'] = injury_df['note_keyword'].map(injury_dictionary )

#------------------------Make plots-------------------------------------------

dataset = injury_df.groupby(['note_keyword'])['Tot_games_missed'].sum()

#fill those 'note_keyword' that are NaN with zeros
dataset.fillna(0, inplace = True)

#match color scheme in stacked bar chart
injury_color_dict = {
        'ankle':'#ff7f0e',
        'knee': '#1f77b4',
        'torso': '#d62728',
        'hamstring': '#2ca02c',
        'foot':'#9467bd',
        'groin': '#2ca02c',
        'toe': '#9467bd',
        'head': '#8c564b',
        'shoulder': '#d62728',
        'quad':'#2ca02c',
        'abdominal': '#d62728',
        'face': '#8c564b',
        'calf': '#ff7f0e',
        'wrist':'#7f7f7f',
        'elbow': '#7f7f7f',
        'finger':'#e377c2',
        'hip': '#2ca02c',
        'achilles': '#ff7f0e',
        'shin':'#ff7f0e',
        'heel': '#9467bd',
        'hand': '#e377c2',
        'arm': '#7f7f7f' 
        }

dataset = dataset.sort_values(ascending = True)
colors = []

#map colors
for n in dataset.index:
    colors.append(injury_color_dict[n])
    
#create plot
ax = dataset.plot(kind = 'barh', color = colors, fig = (6,4))

# Set the x-axis label
ax.set_xlabel("Count of Games Missed", fontsize = 16, weight='bold')

# Set the y-axis label
ax.set_ylabel("Injured Body Part", fontsize =16,weight='bold')


#----------------------Save plot---------------------------------------------
fig = ax.get_figure()
fig.savefig(plot_savepath, bbox_extra_artists=(), bbox_inches='tight',dpi = 300)