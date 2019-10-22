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
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import requests
import numpy as np
import matplotlib.pyplot as plt
import pickle
import pandas as pd

pd.set_option('display.expand_frame_repr', False)

#--------------------------User Inputs---------- ----------------------
#file path for pickle of concatenated/merged mg,il, player stats dataframes
injury_df_filepath =  '../../data/03_processed/mg_il_ps_merged_df.p'

#save path for plot
plot_savepath =  '../../results/01_plots/word_cloud.png'

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
#injury_df = injury_df[~ injury_df['category'].isin(['healthy inactive','rest','sick','other','n/a'])]


#------------------------Make plots-------------------------------------------
note_keywords = injury_df['Notes'][(injury_df['note_keyword'] != 'returned to lineup')]
words = note_keywords.str.cat(sep = ',')

#-------------------------Format---------------------------------------------

# This function takes in your text and your mask and generates a wordcloud. 

stopwords = set(STOPWORDS)
stopwords.add('DTD')
stopwords.add('DNP')
stopwords.add('placed')
stopwords.add('left')
stopwords.add('right')
stopwords.add('IL')

word_cloud = WordCloud(width = 512, height = 512, background_color='black', stopwords=stopwords, collocations = False, colormap = 'Blues').generate(words)
plt.figure(figsize=(10,8),facecolor = 'white', edgecolor='blue')
plt.imshow(word_cloud)
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

#----------------------Save plot---------------------------------------------
word_cloud.to_file(plot_savepath)