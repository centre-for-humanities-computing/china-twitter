'''
VMP 2022-03-13:
figure out which files are problematic
'''

# imports 
import pandas as pd 
import numpy as np
import argparse 
# all files 
from os import listdir
from os.path import isfile, join
import datetime
import networkx as nx

concat = pd.read_csv("/work/cn-some/china-twitter/networks/data/clean/df_full.csv") # load data
concat.head(5)

concat = concat[concat["mentionee"] != concat['mentioner']] # remove self-mentions
concat_sub = concat[(concat["category"] == "Media") | (concat['category'] == 'Diplomat')] # only cited by media or diplomat
weighted_mention = concat_sub.groupby(['mentionee', 'mentioner', 'category', 'category_mentionee']).size().to_frame('weight').reset_index() # weighted
G = nx.from_pandas_edgelist(weighted_mention,source='mentioner',target='mentionee', edge_attr='weight', create_using=nx.DiGraph()) # create network

print('--> generating node & edge attributes')
''' edge attributes '''
edge_weight = nx.get_edge_attributes(G, 'weight').values()

''' node attributes '''
mentioners = weighted_mention[["mentioner", "category"]].drop_duplicates().rename(columns = {'mentioner': 'node'})
mentionees = weighted_mention[["mentionee", "category_mentionee"]].drop_duplicates().rename(columns = {'mentionee': 'node', 'category_mentionee': 'category'})
mentions_category = pd.concat([mentioners, mentionees])
mentions_category = mentions_category.drop_duplicates()
mentions_category["spokespersonHZM"] == 'Diplomat'

issue = 'spokespersonHZM'
concat_sub[concat_sub["mentionee"] == issue]

mentions_category.tail(5)
weighted_mention.head(5)
mentioners.tail(10)
mentionees.tail(10)
# dictionary for category (color)
mentions_category = dict(zip(mentions_category.node, mentions_category.category))
nx.set_node_attributes(G, mentions_category, "category")
category = nx.get_node_attributes(G, 'category').values()
colors = {'Diplomat': 'tab:blue', 'Media': 'tab:orange'}
node_color = [colors.get(x) for x in category]
node_color
category

len(G.nodes(data=True))