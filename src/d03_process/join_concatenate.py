# -*- coding: utf-8 -*-
"""
This script concatentaes the processed missed game dataframe with the process
inactive list dataframe, and then merges (left joins) this concatenated 
dataframe with the player stats dataframe.

It all drops all mg and IL events that correspond to a player returning to a
lineup, as this information is no longer required.

Required inputs:
    -missed_games_processed.p
    -inactive_list_processed.p
    -player_stats_processed.p
    
Outputs:
    -mg_il_ps_merged_df.p
    
@author: evanl
"""
import numpy as np
import pandas as pd
import pickle

pd.set_option('display.expand_frame_repr', False)

#--------------------------User Inputs---------- ----------------------
#file path for pickle pf processed missed games dataframe 
mg_filepath = '../../data/03_processed/missed_games_processed.p'

#file path for pickle of processed inactive list events dataframe 
il_filepath = '../../data/03_processed/inactive_list_processed.p'

#file path for pickle of processed player stats dataframe
ps_filepath =  '../../data/03_processed/player_stats_processed.p'

#file path for pickle of concatenated/merged mg,il, player stats dataframes
merged_savepath =  '../../data/03_processed/mg_il_ps_merged_df.p'

#-------------------------Load Files------------------------------------------
#load missed games dataframe
mg_processed_df = pickle.load(open(mg_filepath, "rb" ) )

#load inactive list dataframe
il_processed_df = pickle.load(open(il_filepath, "rb" ) )

#load player stats dataframe
ps_processed_df = pickle.load(open(ps_filepath, "rb" ) )

#------------------------Concatenate MG and IL -------------------------

mg_il_concat_df = pd.concat([mg_processed_df,il_processed_df], axis = 0)


#--------------Merge Player Stats df with MG/IL df------------------------

#Left merge on columns 'Player', 'Year','Season'
mg_il_concat_ps_merge_df =  pd.merge(mg_il_concat_df, ps_processed_df, how = 'left', on=['Player', 'Year','Season'])

#-----------------Clean up 'Team' column after merge-------------------------

#Keep 'Team_x' column, drop 'Team_y' column (less accurate)
mg_il_concat_ps_merge_df.drop(['Team_y'],axis =1)

#Rename 'Team_x'
mg_il_concat_ps_merge_df.rename(columns ={'Team_x':'Team'}, inplace = True)

#-----------------Convert 'Game_number' to dtype int-----------------------
mg_il_concat_ps_merge_df['Game_number'] = mg_il_concat_ps_merge_df['Game_number'].astype(int)

#-----------------------Save Data-----------------------------
print('Saving files......')
#save file
pickle.dump(mg_il_concat_ps_merge_df, open(merged_savepath, "wb" ) )        
print('Finished')   
