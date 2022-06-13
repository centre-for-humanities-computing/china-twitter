'''
VMP 2022-06-13: 
scoring of our data set 
'''

# packages
import pandas as pd 
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

## load data ##
network_dat = pd.read_csv("/work/cn-some/china-twitter/networks/data/clean/df_full.csv")
network_dat = network_dat[["mentionee", "mentioner", "category_mentionee"]]
network_dat = network_dat.drop_duplicates()
metadata = pd.read_csv("/work/cn-some/china-twitter/bot-detection/curated_data/mentioner_fofo.csv")

### dataset overall 
network_meta = network_dat.merge(metadata, on = "mentioner", how = "inner")
len(network_dat) # 6.014.742
len(network_meta) # 3.852.595 (hmmm, not quite all of the records

### overall & diplomat / media
network_overall = network_meta[["mentioner", "followers_mentioner", "following_mentioner"]].drop_duplicates()
network_media = network_meta[network_meta["category_mentionee"] == "Media"][["mentioner", "followers_mentioner", "following_mentioner"]].drop_duplicates()
network_diplomat = network_meta[network_meta["category_mentionee"] == "Diplomat"][["mentioner", "followers_mentioner", "following_mentioner"]].drop_duplicates()

### save everything
network_overall.to_csv("/work/cn-some/china-twitter/bot-detection/curated_data/overall_data.csv", index=False)
network_media.to_csv("/work/cn-some/china-twitter/bot-detection/curated_data/media_data.csv", index=False)
network_diplomat.to_csv("/work/cn-some/china-twitter/bot-detection/curated_data/diplomat_data.csv", index=False)