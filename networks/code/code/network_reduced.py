'''
2022-01-25 VMP:
Not used at the moment.
extremely simplified plot types. 
(media, diplomat) & (media, diplomat, other).
This is just somehow impossible to get nice in terms of drawing. 
Pretty annoying issue, would actually really like to have good solution. 
'''

# imports 
import pandas as pd 
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt
from statistics import median
import math
from matplotlib.lines import Line2D

# load 
concat = pd.read_csv("/work/cn-some/mentions_net/data/concat_new.csv")

# remove self-mentions (???)
concat = concat[concat["mentionee"] != concat['mentioner']]

# only cited by media and/or diplomat for the focus case. 
concat_sub = concat[(concat["category"] == "Media") | (concat['category'] == 'Diplomat')]
concat_sub.dtypes
# weighted mentions 
weighted_mention = concat_sub.groupby(['mentionee', 'mentioner', 'category', 'category_mentionee']).size().to_frame('weight').reset_index() 
focus_reduced = weighted_mention.groupby(['category', 'category_mentionee'])['weight'].sum().to_frame('weight').reset_index()

# create network
G = nx.from_pandas_edgelist(focus_reduced,source='category',target='category_mentionee', edge_attr='weight', create_using=nx.DiGraph())

## edge properties (weight)
weight = nx.get_edge_attributes(G, 'weight').values() 

## node properties (in+out degree)
degrees = {node:val for (node, val) in G.degree()}
nx.set_node_attributes(G, degrees, "degree")
degree_data = nx.get_node_attributes(G, 'degree').values()

'''
# setup 
fig, ax = plt.subplots(figsize=(12, 12), dpi=200, facecolor='w', edgecolor='k')
plt.axis("off")

# position & manual tweaking
pos = nx.spring_layout(G, seed=8)

# draw stuff 
node_size = [x/100 for x in degree_data] # only difference
edge_width = [x/100 for x in weight]
nx.draw_networkx_nodes(G, pos, node_size = node_size) #, node_color = node_color)
nx.draw_networkx_edges(G, pos, width = edge_width, alpha =1) #, edge_color = edge_col)
'''

# https://stackoverflow.com/questions/22785849/drawing-multiple-edges-between-two-nodes-with-networkx

node_positions = {
    'Diplomat' : np.array([0.2, 0.8]),
    'Media' : np.array([0.8, 0.2]),
}

edge_labels = { # weight
    ('Diplomat', 'Diplomat') : 10395,
    ('Diplomat', 'Media') : 1325,
    ('Media', 'Diplomat') : 845,
    ('Media', 'Media') : 832
}

fig, ax = plt.subplots(figsize=(14,14))

Graph(G, node_labels=True, edge_labels=edge_labels,
      edge_label_fontdict=dict(size=12, fontweight='bold'),
      node_layout=node_positions, 
      edge_layout='curved', # curved
      node_size=6, edge_width=4, arrows=True, ax=ax)

plt.savefig("/work/cn-some/mentions_net/fig/network_reduced.png")
