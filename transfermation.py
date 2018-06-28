#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 20:18:25 2018
This script load in txt file and convert it xlsx
@author: Xun
"""

import pandas as pd

df_load = pd.read_fwf('data/Alliance-ga.txt', skiprows=3,header=None)

df_load_data = df_load[5:]

df_title = pd.read_excel('data/license data_09212016.xlsx')

df_load_data.columns = df_title.columns

df_load_data['new_flag'] = df_load_data['Status'].apply(lambda x: 0 if pd.isnull(x) else 1)
df_load_data['obs'] = df_load_data['new_flag'].cumsum()
df_load_data.fillna('',inplace=True)

df_load_data_ent = df_load_data[['obs','new_flag', 'History Date', 'Date Alliance Terminated', 'Alliance Date Announced',
       'Date Effective', 'Date Sought', 'Alliance Date Announced.1',
       'Participants in Venture / Alliance (Short Name)',
       'Business Description ', 'Participant Primary SIC Code',
       'Participant Nation', 'Participant State Code',
       'Participant Ultimate Parent Name',
       'Participant Ultimate Parent Nation',
       'Participant Ultimate Parent Primary SIC Code', 'Alliance Deal Name','Technology Transfer',
       'Primary SIC Code of Alliance', 'Nation of Alliance',
       'State Description', 'Status', 'Transaction Type',
       'Activity Description', 'Joint Venture Flag', 'Cross Border Alliance',
       'Percent Ownership by Participant',
       'Parti. CUSIP', 'Participant CUSIP', 'Ultimate Parent CUSIP',
       'Participant Ultimate Parent CUSIP', 'Participant Parent CUSIP',
       'Date Alliance Signed Estimated Flag',
       'Date of announcement Estimated Flag',
       'Date Alliance Terminated Estiamted Flag']]
df_load_data_ent = df_load_data_ent[df_load_data_ent['Participants in Venture / Alliance (Short Name)']!='']

# Process Long Text
df_load_data_txt = df_load_data[['obs','new_flag','Long Business Description',
                                 'Deal Text','Capitalization Text']]
df_concat = df_load_data_txt.groupby(['obs']).agg(lambda x: ' '.join(x))
df_concat.reset_index(inplace=True)

# Merge!
df_load_data_ent['case_index'] = df_load_data_ent['obs']*df_load_data_ent['new_flag']
df_final = pd.merge(df_load_data_ent, df_concat, how='left', left_on='case_index', right_on='obs')

df_final = df_final[df_title.columns]

df_final.to_excel('data/license data_09212016_processed_v2.xlsx', index=False)