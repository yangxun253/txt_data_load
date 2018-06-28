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

df_concat = df_load_data.groupby(['obs']).agg(lambda x: ' '.join(x))
df_concat.to_excel('data/license data_09212016_processed.xlsx', index=False)