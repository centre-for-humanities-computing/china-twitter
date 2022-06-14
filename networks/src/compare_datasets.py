'''
VMP 2022-06-15
'''

import pandas as pd 

# read data sets 
d_filtered = pd.read_csv("/work/cn-some/china-twitter/networks/data/clean/df_filtered.csv")
d_full = pd.read_csv("/work/cn-some/china-twitter/networks/data/clean/df_full.csv")

# how large are the data sets 
len(d_filtered) # 14.685.465
len(d_full) # 26.321.014

# which are the largest in each 
top_filtered = d_filtered.groupby('mentionee').size().reset_index(name = 'count').sort_values('count', ascending=False).head(10)
top_full = d_full.groupby('mentionee').size().reset_index(name = 'count').sort_values('count', ascending=False).head(10)

## ordering different: same handles
top_filtered.head(10)
top_full.head(10)

# check dates
d_filtered["created_at"].min() # good
d_filtered["created_at"].max() # good 
d_full["created_at"].min() # too early (the problem)
d_full["created_at"].max() # good 