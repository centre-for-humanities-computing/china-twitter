'''
VMP 2022-02-18: 
Not used in the analysis as of now. 
If we get more hours this would be good to develop. 
Basically we just want a top "from --> to" plot.
'''

import pandas as pd 
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt
from statistics import median
import math
from matplotlib.lines import Line2D
import argparse 
from pathlib import Path
    
# preprocessing 
concat = pd.read_csv("/work/cn-some/mentions_net/data/concat_new.csv") # load data
concat = concat[concat["mentionee"] != concat['mentioner']] # remove self-mentions
concat_sub = concat[(concat["category"] == "Media") | (concat['category'] == 'Diplomat')] # only cited by media or diplomat
weighted_mention = concat_sub.groupby(['mentionee', 'mentioner', 'category', 'category_mentionee']).size().to_frame('weight').reset_index() # weighted
weighted_mention.sort_values('weight', ascending=False)

weighted_mention.head(5)

# plot 
fig, ax = plt.subplots(dpi=150)
df_merged = df_merged.sort_values('degree_total', ascending=False)
df_plot = df_merged[["id", "in_degree", "out_degree"]].head(10)
df_plot.index = df_plot["id"]
df_plot.plot.bar(stacked=True)
plt.title('Top 10 degree (sub-network)')
plt.xlabel('Handle')
plt.ylabel('Degree')
plt.savefig("/work/cn-some/mentions_net/fig/summary_focus_degree.png", bbox_inches='tight')