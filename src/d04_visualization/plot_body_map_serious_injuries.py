# -*- coding: utf-8 -*-
"""
This script creates a stacked bar chart of missed games due to injury. Each 
bar represents a year, each stack with in the corrresponds to an injury "category"
or "keyword".

Required inputs:
    -mg_il_ps_merged_df.p
    
Outputs:
    -stacked bar chart
    
@author: evanl
"""

import pandas as pd
import pickle
import matplotlib.pyplot as plt

pd.set_option('display.expand_frame_repr', False)

#--------------------------User Inputs---------- ----------------------
#file path for pickle of concatenated/merged mg,il, player stats dataframes
injury_df_filepath =  '../../data/03_processed/mg_il_ps_merged_df.p'

#path for basketball player silhouette .png
image_filepath =  '../../references/02_images/durant_silhouette.png'

#year to plot
year = 2018

#save path for plot
plot_savepath =  '../../results/01_plots/body_map_serious_injuries{}.png'.format(year)

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
injury_df = injury_df[injury_df['Tot_games_missed'] > 15.0]

#Exclude those 'injuries' which are not relevant (healthy scratches, rest, sick, n/a, other)
injury_df = injury_df[~ injury_df['category'].isin(['healthy inactive','rest','sick','other','n/a'])]

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

dataset = injury_df.groupby(['Year','note_keyword'])['Tot_games_missed'].sum().sort_values(ascending=False).unstack()

#fill those 'note_keyword' that are NaN with zeros
dataset.fillna(0, inplace = True)

#location on image to plot marker
location_x = {
        'ankle':125,
        'knee': 420,
        'torso': 250,
        'hamstring': 420,
        'foot':100,
        'groin': 350,
        'toe': 600,
        'head': 100,
        'shoulder': 250,
        'quad':220,
        'abdominal': 300,
        'face': 80,
        'calf': 170,
        'wrist':480,
        'elbow': 400,
        'finger': 60,
        'hip': 360,
        'achilles': 650,
        'shin':520,
        'heel': 160,
        'hand': 70,
        'arm': 340    
        }

location_y = {
        'ankle':650,
        'knee': 600,
        'torso': 250,
        'hamstring': 500,
        'foot':700,
        'groin': 450,
        'toe': 700,
        'head': 100,
        'shoulder': 120,
        'quad':380,
        'abdominal': 300,
        'face': 180,
        'calf': 500,
        'wrist':120,
        'elbow': 180,
        'finger': 610,
        'hip': 350,
        'achilles': 620,
        'shin':630,
        'heel': 700,
        'hand': 570,
        'arm': 160 
        }

#match color scheme in stacked bar chart
color_dict = {
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

#Set max size of marker
max_size = 2000
#Max value of missed games; use to normalize marker size
max_value = dataset.values.max()

#Adjust DPI to control size of plot    
dpi = 110
im_data = plt.imread(image_filepath)
height, width, depth = im_data.shape

# Adjust size of figure 
figsize = width / float(dpi), height / float(dpi)

# Create a figure of the right size with one axes that takes up the full figure
fig = plt.figure(figsize=figsize)
ax = fig.add_axes([0, 0, 1, 1])

# Hide spines, ticks, etc.
ax.axis('on')

# Display the image.
ax.imshow(im_data, cmap='gray')

##Uncomment code to plot axis grids
#ax.grid()
#ax.minorticks_on()
##Customize the minor grid
#ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
#plt.axis('on')

#plot a marker with size proportional to number of missed games
for body_part in dataset.columns:
    plt.scatter(location_x[body_part], location_y[body_part], s=((dataset[body_part][year])/max_value*max_size), c = color_dict[body_part]) 

#manually create a legend/key
plt.scatter(550, 400, s=(1000/max_value*max_size), marker='o', facecolors='none', edgecolors='k',linewidths=3)    
ax.text(0.85, 0.46, str(int(1000)), transform=ax.transAxes, fontsize=18, weight ='bold', verticalalignment='top')

plt.scatter(550, 320, s=(500/max_value*max_size), marker='o', facecolors='none', edgecolors='k',linewidths=3)    
ax.text(0.85, 0.57, str(int(500)), transform=ax.transAxes, fontsize=18, weight ='bold', verticalalignment='top')

plt.scatter(550, 260, s=(200/max_value*max_size), marker='o', facecolors='none', edgecolors='k',linewidths=3)    
ax.text(0.85, 0.65, str(int(200)), transform=ax.transAxes, fontsize=18, weight ='bold', verticalalignment='top')
 
# text box one
ax.text(0.60, 0.77, ('{}/{} Season '.format(year, (year+1))), transform=ax.transAxes, fontsize=18, weight ='bold', verticalalignment='top')    
# text box two
ax.text(0.685, 0.73, 'Missed Games', transform=ax.transAxes, fontsize=18, weight ='bold', verticalalignment='top')    

# text box two
ax.text(0.0000, 0.99, 'Injury Duration > 15 games', transform=ax.transAxes, fontsize=16, weight ='bold', verticalalignment='top')   

plt.axis('off')
plt.show()

#----------------------Save plot---------------------------------------------
fig = ax.get_figure()
fig.savefig(plot_savepath, dpi = 300)