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

top_filtered.head(10)
top_full.head(10)

## NB: ordering is different, but the top-10 is largely the same accounts. 