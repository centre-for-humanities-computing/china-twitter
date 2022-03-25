'''
VMP 2022-03-25: not used in the paper/analysis.
Used for testing networkx functionality related to
the order that edges and nodes are plotted/drawn.
Kept for reference. 
'''

import pandas as pd 
import networkx as nx 

# data
d = pd.DataFrame({
    'from': ['A', 'A', 'B', 'C', 'D', 'D'],
    'to': ['B', 'C', 'C', 'A', 'C', 'E'],
    'weight': [1, 1, 2, 2, 3, 1]})

# network
G = nx.from_pandas_edgelist(
    d, 
    source='from',
    target='to', 
    edge_attr='weight', 
    create_using=nx.DiGraph())

# degree
degree_dct = {node:val for (node, val) in G.degree(weight='weight')}
nx.set_node_attributes(G, degree_dct, "degree")

color_dct = {
    'A': {'color': 'red'}, 
    'B': {'color': 'blue'}, 
    'C': {'color': 'black'}, 
    'D': {'color': 'green'}, 
    'E': {'color': 'purple'}
}
nx.set_node_attributes(G, color_dct)
col = nx.get_node_attributes(G, 'color')

# sorted dictionary
node_dict = dict(G.nodes(data=True))
node_dict_sorted = dict(sorted(node_dict.items(), key = lambda x: x[1]['degree'], reverse=True))

# extract node information
nodelst = []
nodelst_color = []
nodelst_weight = []
for node, data in node_dict_sorted.items(): 
    nodelst.append(node)
    color = data.get("color")
    weight = data.get("degree")
    nodelst_color.append(color)
    nodelst_weight.append(weight)

# set edge attributes
attrs = {
    ('A', 'B'): {"color": 'blue', "weight": 2}, 
    ('A', 'C'): {"color": 'blue', "weight": 4},
    ('B', 'C'): {"color": 'green', "weight": 3},
    ('C', 'A'): {"color": "green", "weight": 1},
    ('D', 'C'): {"color": "black", "weight": 1},
    ('D', 'E'): {"color": "black", "weight": 5}}

nx.set_edge_attributes(G, attrs)

# extract each
edge_weight = nx.get_edge_attributes(G, 'weight')
edge_color = nx.get_edge_attributes(G, 'color')

# put them together 
from collections import defaultdict
edge_dict = defaultdict(dict)
for d, name in zip([edge_weight, edge_color], ['weight', 'color']): # you can list as many input dicts as you want here
    for key, value in d.items():
        edge_dict[key][name] = value
edge_dict = dict(edge_dict)
edge_dict_sorted = dict(sorted(edge_dict.items(), key = lambda x: x[1]['weight'], reverse=True))

# extract edge information
edgelst = []
edgelst_color = []
edgelst_weight = []
for edge, data in edge_dict_sorted.items(): 
    edgelst.append(edge)
    color = data.get("color")
    weight = data.get("weight")
    edgelst_color.append(color)
    edgelst_weight.append(weight)


# test whether smaller nodes are on top of larger nodes (yes)
nodelst_weight_scaled = [x*1500 for x in nodelst_weight]

k = 0.5
seed = 5
pos = nx.spring_layout(G, k=k, iterations=30, seed=seed)
nx.draw_networkx_nodes(G, pos, nodelist = nodelst, node_size = nodelst_weight_scaled, node_color = nodelst_color)


# test whether smaller edges are on top of larger edges (yes)
nodelst_weight_scaled = [x*20 for x in nodelst_weight]
edgelst_weight_scaled = [x*3 for x in edgelst_weight]

k = 0.5
seed = 5
pos = nx.spring_layout(G, k=k, iterations=30, seed=seed)
nx.draw_networkx_nodes(G, pos, nodelist = nodelst, node_size = nodelst_weight_scaled, node_color = nodelst_color)
nx.draw_networkx_edges(G, pos, edgelist = edgelst, width = edgelst_weight_scaled, edge_color = edgelst_color, arrows=False)
