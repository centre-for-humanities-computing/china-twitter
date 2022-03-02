'''
VMP 2022-02-18:
compare concat_new vs. df_clean
not actually used anywhere (just sanity check)
'''

# import stuff
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
import datetime

# concat_new vs. df_clean 
df_clean = pd.read_csv("/work/cn-some/mentions_net/data/df_clean.csv")
df_concat = pd.read_csv("/work/cn-some/mentions_net/data/concat_new.csv")
df_full = pd.read_csv("/work/cn-some/mentions_net/data/df_full.csv")

# volume of data
df_clean_rows = len(df_clean) 
df_concat_rows = len(df_concat) 
df_full_rows = len(df_full)

# check duplication and self-referencing 
## self-reference (not a big thing)
df_clean_no_self_ref = len(df_clean[df_clean["mentioner"] != df_clean["mentionee"]]) 
df_concat_no_self_ref = len(df_concat[df_concat["mentioner"] != df_concat["mentionee"]])
df_full_no_self_ref = len(df_full[df_full["mentioner"] != df_full["mentionee"]])

## duplication (unfortunately tweet-id is fucked)
df_clean_no_duplication = len(df_clean[["mentionee", "mentioner", "retweet", "text", "category", "category_mentionee"]].drop_duplicates())
df_concat_no_duplication = len(df_concat[["mentionee", "mentioner", "retweet", "text", "category", "category_mentionee"]].drop_duplicates())
df_full_no_duplication = len(df_full[["mentionee", "mentioner", "retweet", "text", "category", "category_mentionee"]].drop_duplicates())

# print stuff
div = 1000000
r = 2
print(f"clean rows: {round(df_clean_rows/div, r)}M") # 14.53M
print(f"concat rows: {round(df_concat_rows/div, r)}M") # 24.95M
print(f"full rows: {round(df_full_rows/div, r)}M") # 26.07M
print(f"clean (no self-ref): {round(df_clean_no_self_ref/div, r)}M") # 14.53M
print(f"concat (no self-ref): {round(df_concat_no_self_ref/div, r)}M") # 24.94M
print(f"full (no self-ref): {round(df_full_no_self_ref/div, r)}M") #26.06M
print(f"clean (no duplication): {round(df_clean_no_duplication/div, r)}M") # 14.31M
print(f"concat (no duplication): {round(df_concat_no_duplication/div, r)}M") # 24.53M
print(f"full (no duplication): {round(df_full_no_duplication/div, r)}M") #25.62M

# volume of mentioners
df_clean.groupby('mentionee').size().reset_index(name = 'count').sort_values('count', ascending=False).head(10) # globaltimesnews, XHNews, zlj517, Huxijin_GT, CGTNOfficial, ...
df_concat.groupby('mentionee').size().reset_index(name = 'count').sort_values('count', ascending=False).head(10) # CHNews, CGTNOfficial, globaltimesnews, zlj517, ChinaDaily, ...
df_full.groupby('mentionee').size().reset_index(name = 'count').sort_values('count', ascending=False).head(10) # XHNews, CGTNOfficial, globaltimesnews, zlj...

# is it because it changes over time? 
df_full["created_at"] = pd.to_datetime(df_full["created_at"]).dt.date
late_data = df_full[df_full["created_at"] >= datetime.date(2021, 2, 28)]
early_data = df_full[df_full["created_at"] <= datetime.date(2019, 11, 1)]

len(late_data) # late is not the driver (just by volume)
len(early_data) # okay, early is the driver

early_data.groupby('mentionee').size().reset_index(name='count').sort_values('count', ascending=False).head(10) # XHNews, CGTNOfficial, zlj517, ChinaDaily
early_data["created_at"].min() # all the way from 2009
