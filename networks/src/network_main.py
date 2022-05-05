'''
main document for plot (updated 2022-02-01 VMP).
'''

# imports 
import pandas as pd 
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt
from statistics import median
import math
from matplotlib.lines import Line2D
import argparse 
from pathlib import Path
from collections import defaultdict

''' degree: make smarter '''

def degree_information(G, method, metric):
    '''
    G: <networkx.classes.digraph.DiGraph
    method: G.degree() or variants 
    metric: <str> e.g. "weighted_degree" 
    '''

    degree = {node:val for (node, val) in method}
    nx.set_node_attributes(G, degree, metric)

''' sort values '''

#### labels ####
# labels mentions 
def get_labels(G, type_str, type_lst, n_labels):
    '''
    type_str: <str> e.g. "mentions" 
    type_lst: <list> corresponding.
    n_labels: <int> number of labels
    '''
    # sort list and take top 
    focus_handles = [
        'XHNews', 
        'CGTNOfficial', 
        'ChinaDaily', 
        'globaltimesnews',  
        'SpokespersonCHN', 
        'MFA_China',
        'zlj517',
        #'PDChina', 
        #'AmbLiuXiaoMing', 
        #'AmbCuiTianKai',
        #'HuXijin_GT',
        #'CNS51952',
        #'ChnEmbassy_jp'
    ]
    
    lst_sorted = sorted(type_lst, reverse=True)
    cutoff = lst_sorted[n_labels]
    
    # loop over them and assign labels to greater than cutoff 
    labels = nx.get_node_attributes(G, type_str)
    labeldict = {}

    for key, val in labels.items(): 

        if key in focus_handles: 
            labeldict[key] = key

        elif val > cutoff: 
            labeldict[key] = key
        
        else: 
            labeldict[key] = ''
    
    return labeldict 

#### general plot setup #### 
def get_legend(node_size_list, colors_dct):
    node_median = median(node_size_list) 
    lines = [Line2D([0], [0], linewidth=0, markersize = math.sqrt(node_median), color = colors_dct.get('Diplomat'), marker='o'), 
            Line2D([0], [0], linewidth=0, markersize = math.sqrt(node_median), color = colors_dct.get('Media'), marker='o')] 
    labels = ['Diplomat', 'Media']
    return lines, labels

def nudge_position(pos, nudge_triple):
    '''
    pos: nx.spring_layout
    nudge_triple: <list> list of triples with name, x, y. 
    '''
    for name, x, y in nudge_triple:
        pos[name] += (x, y) 
    return pos

def sort_dictionary(d, sort_val): 
    '''
    d: <dict> 
    sort_val: <str>
    '''
    d_sort = dict(sorted(d.items(), key = lambda x: x[1][sort_val], reverse=True))
    return d_sort

def add_color(dct_nodecolor, dct_nodeedgecolor, category_lst): 
    '''
    dct_nodecolor: <dict>
    dct_nodeedgecolor: <dict>
    category_list: <list>
    '''
    node_color = [dct_nodecolor.get(x) for x in category_lst] 
    node_edgecolor = [dct_nodeedgecolor.get(x) for x in category_lst]
    return node_color, node_edgecolor 

# extract values for each network
def extract_values(dct, color_var, size_var, reverse = True): 
    '''
    dct: <dict> (sorted)
    color_var: <str> color variable (e.g. "color" or "category")
    size_var: <str> size variable (e.g. "degree" or "weight")
    '''
    lst = []
    lst_color = []
    lst_size = []
    for netobj, data in dct.items(): 
        lst.append(netobj)
        color = data.get(color_var)
        size = data.get(size_var)
        lst_color.append(color)
        lst_size.append(size)
    return lst, lst_size, lst_color
    
def extract_edgedict(dict_lst, var_lst, sort_var): 
    '''
    input:
        dict_lst: <list> list of dictionaries
        var_lst: <list> list of string
        sort_var: <string> var to sort by

    assumes: 
        len(dict_lst) == len(var_lst)

    returns: 
        sorted dictionary of edge data
    '''

    edge_dict = defaultdict(dict)
    for d, name in zip(dict_lst, var_lst): # you can list as many input dicts as you want here
        for key, value in d.items():
            edge_dict[key][name] = value
    edge_dict = dict(edge_dict)
    edge_dict_sorted = dict(sorted(edge_dict.items(), key = lambda x: x[1][sort_var], reverse=True))
    return edge_dict_sorted 

#### plot 1 ####
def plot_network(G, nodelst, edgelst, color_dct, node_color, nodeedge_color, edge_color, labeldict, node_size_lst, edge_width_lst, node_divisor, edge_divisor, title, filename, outfolder, seed = 8, k = 2, nudge_triple = False): 

    '''
    G: <networkx.classes.digraph.DiGraph> the graph
    node_size_lst: <list> node sizes 
    edge_width_lst: <list> edge width
    node_divisor: <int/float> scaling for all node sizes 
    edge_divisor: <int/float> scaling for all edges 
    title: <str> plot title 
    filename: <str> filename 
    '''

    # setup 
    fig, ax = plt.subplots(figsize=(2.5, 2.5), dpi=300, facecolor='w', edgecolor='k')
    plt.axis("off")

    # position & manual tweaking
    pos = nx.spring_layout(G, k=k, iterations=30, seed=seed)
    if nudge_triple: 
        pos = nudge_position(pos, nudge_triple)

    # set up 
    node_size = [x/node_divisor for x in node_size_lst]
    edge_width =  [x/edge_divisor for x in edge_width_lst]

    # draw it 
    nx.draw_networkx_nodes(G, pos, nodelist = nodelst, node_size=node_size, node_color=node_color, edgecolors = nodeedge_color, linewidths=0.3) #, node_size = node_size, node_color = node_color)
    nx.draw_networkx_edges(G, pos, edgelist = edgelst, width = edge_width, alpha = 0.5, edge_color = edge_color, arrows=False)

    # labels 
    label_options = {"edgecolor": "none", "facecolor": "white", "alpha": 0}
    nx.draw_networkx_labels(G,pos,labels=labeldict,font_size=3, bbox=label_options, font_weight = 'bold')

    # formatting & save
    lines, labels = get_legend(node_size, color_dct)
    fig.legend(lines, labels, loc = 'lower left', labelspacing = 1.2, fontsize = 6, frameon = False)
    plt.tight_layout()
    plt.savefig(f"{outfolder}/{filename}_seed{seed}_k{k}.png", bbox_inches='tight')

def main(n_labels, infile, outfolder): 
    print(infile)
    ''' 1. vars '''
    seed = 11
    k = 1.8
    edge_mult = 4.5
    c_node = {'Diplomat': '#6baed6', 'Media': '#fd8d3c'} # blue: https://www.color-hex.com/color-palette/17597 , orange: https://www.color-hex.com/color-palette/17665
    c_nodeedge = {'Diplomat': '#2171b5', 'Media': '#d94701'} #blue: https://www.color-hex.com/color-palette/17597 , orange: https://www.color-hex.com/color-palette/17665
    
    ''' 2. setup/create network '''
    print('--- starting: visualize networks')
    print('--> reading data & creating network')
    concat = pd.read_csv(f"{infile}") # load data
    concat = concat[concat["mentionee"] != concat['mentioner']] # remove self-mentions
    concat_sub = concat[(concat["category"] == "Media") | (concat['category'] == 'Diplomat')] # only cited by media or diplomat
    weighted_mention = concat_sub.groupby(['mentionee', 'mentioner', 'category', 'category_mentionee']).size().to_frame('weight').reset_index() # weighted
    G = nx.from_pandas_edgelist(weighted_mention,source='mentioner',target='mentionee', edge_attr='weight', create_using=nx.DiGraph()) # create network

    print('--> adding node & edge attributes')

    ''' 3. create and set node attributes '''
    # mentions for color 
    mentioners = weighted_mention[["mentioner", "category"]].drop_duplicates().rename(columns = {'mentioner': 'node'})
    mentionees = weighted_mention[["mentionee", "category_mentionee"]].drop_duplicates().rename(columns = {'mentionee': 'node', 'category_mentionee': 'category'})
    mentions_category = pd.concat([mentioners, mentionees])
    mentions_category = mentions_category.drop_duplicates()
    mentions_category = dict(zip(mentions_category.node, mentions_category.category))
    nx.set_node_attributes(G, mentions_category, "category")

    # size: based on mentions in total dataset
    G_nodes = list(G.nodes())
    size_frame = concat.groupby('mentionee').size().to_frame('mentions').reset_index()
    mentionee_size = size_frame[size_frame["mentionee"].isin(G_nodes)]
    mentionee_size_dct = dict(zip(mentionee_size.mentionee, mentionee_size.mentions))
    nx.set_node_attributes(G, mentionee_size_dct, "mentions")

    # size based on various kinds of degree 
    degree_information(G, G.degree(weight=None), "unweighted_degree")
    degree_information(G, G.degree(weight='weight'), "weighted_degree")
    degree_information(G, G.in_degree(weight='weight'), "in_degree")
    degree_information(G, G.out_degree(weight='weight'), "out_degree")
    
    ''' 4. create / set edge attributes '''
    # edge color 
    for i, j in G.edges():
        i_cat = G.nodes[i]["category"]
        j_cat = G.nodes[j]["category"]

        if i_cat == 'Diplomat' and j_cat == 'Diplomat':
            edge_col = c_node.get('Diplomat')
        
        elif i_cat == 'Media' and j_cat == 'Media': 
            edge_col = c_node.get('Media')

        else: 
            edge_col = 'tab:grey'

        G[i][j]['color'] = edge_col

    ''' 5. sort node dictionaries '''
    # different sorts 
    dct_node = dict(G.nodes(data=True))
    dct_mention = sort_dictionary(dct_node, 'mentions')
    dct_unweighted = sort_dictionary(dct_node, 'unweighted_degree')
    dct_weighted = sort_dictionary(dct_node, "weighted_degree")
    dct_indegree = sort_dictionary(dct_node, "in_degree")
    dct_outdegree = sort_dictionary(dct_node, "out_degree") 

    ''' 6. extract values from node dictionaries '''
    # extract node values 
    nodelst_mentions, nodesize_mentions, nodecategory_mentions = extract_values(dct_mention, "category", "mentions")
    nodelst_unweighted, nodesize_unweighted, nodecategory_unweighted = extract_values(dct_unweighted, "category", "unweighted_degree")
    nodelst_weighted, nodesize_weighted, nodecategory_weighted = extract_values(dct_weighted, "category", "weighted_degree")
    nodelst_indegree, nodesize_indegree, nodecategory_indegree = extract_values(dct_indegree, "category", "in_degree")
    nodelst_outdegree, nodesize_outdegree, nodecategory_outdegree = extract_values(dct_outdegree, "category", "out_degree")

    ''' 6.1. category --> color '''
    nodecolor_mentions, nodeedgecolor_mentions = add_color(c_node, c_nodeedge, nodecategory_mentions)
    nodecolor_unweighted, nodeedgecolor_unweighted = add_color(c_node, c_nodeedge, nodecategory_unweighted)
    nodecolor_weighted, nodeedgecolor_weighted = add_color(c_node, c_nodeedge, nodecategory_weighted)
    nodecolor_indegree, nodeedgecolor_indegree = add_color(c_node, c_nodeedge, nodecategory_indegree)
    nodecolor_outdegree, nodeedgecolor_outdegree = add_color(c_node, c_nodeedge, nodecategory_outdegree)

    ''' 7. prepare edge dictionary '''
    # prepare edge dictionary
    edgeattr_color = nx.get_edge_attributes(G, 'color')
    edgeattr_weight = nx.get_edge_attributes(G, 'weight')
    edge_dict_list = [edgeattr_color, edgeattr_weight]
    edge_var_list = ['color', 'weight']
    dct_edge = extract_edgedict(edge_dict_list, edge_var_list, "weight")

    ''' 8. extract values from edge dictionary '''
    edgelst, edgesize, edgecolor = extract_values(dct_edge, "color", "weight")
    
    ## labels ---> next step 
    n_labels = args['nlabels'] 
    labeldict_mentions = get_labels(G, 'mentions', nodesize_mentions, n_labels)
    labeldict_unweighted = get_labels(G, 'unweighted_degree', nodesize_unweighted, n_labels)
    labeldict_weighted = get_labels(G, 'weighted_degree', nodesize_weighted, n_labels)
    labeldict_indegree = get_labels(G, 'in_degree', nodesize_indegree, n_labels)
    labeldict_outdegree = get_labels(G, 'out_degree', nodesize_outdegree, n_labels - 4) # special treatment

    ''' mentions '''
    print('--> generating mentions plot')
    node_divisor = 600*17
    edge_divisor = 100*edge_mult
    title = 'Diplomats and Media sub-network (nodesize: total number of mentions)'
    filename = 'network_focus_mentions'
    
    ## fix the fact that we now have two files 
    if infile == "/work/cn-some/china-twitter/networks/data/clean/df_full.csv":
        nudge_triple = [ # nudge triple specifically for this data & seed
            ('MFA_China', 0, 0.1),
            ('AmbassadeChine', 0, 0.05),
            ('PDChina', 0, 0.05),
            ('ChnMission', -0.05, 0.1),
            ('consulat_de', -0.05, 0),
            ('chenweihua', -0.05, 0)
            ] 
    
    if infile == "/work/cn-some/china-twitter/networks/data/clean/rt_df_full.csv":
        nudge_triple = [ # nudge triple specifically for this data and seed
            ('consulat_de', -0.05, 0),
            ('Chinamission2un', 0.05, 0),
            ('zlj517', -0.1, -0.05),
            ('chenweihua', 0.05, 0.1),
            ('SpokespersonCHN', 0.05, 0.05),
            ('AmbassadeChine', -0.05, 0.05),
            ('CHN_UN_NY', 0.05, -0.05),
            ('PDChina', 0.05, 0.05)
        ]

    plot_network(
        G = G, 
        nodelst = nodelst_mentions,
        edgelst = edgelst,
        color_dct = c_node,
        node_color = nodecolor_mentions,
        nodeedge_color = nodeedgecolor_mentions,
        edge_color = edgecolor,
        labeldict = labeldict_mentions,
        node_size_lst = nodesize_mentions, 
        edge_width_lst = edgesize,
        node_divisor = node_divisor,
        edge_divisor = edge_divisor,
        title = title,
        filename = filename,
        outfolder = outfolder,
        k = k,
        seed = seed,
        nudge_triple = nudge_triple)

    ## unweighted degree
    print('--> generating unweighted degree plot')
    node_divisor = 0.05*10
    edge_divisor = 100*edge_mult
    title = 'Diplomats and Media sub-network (nodesize: number of neighbors)'
    filename = 'network_focus_unweighted_degree'

    plot_network(
        G = G, 
        nodelst = nodelst_unweighted,
        edgelst = edgelst,
        color_dct = c_node,
        node_color = nodecolor_unweighted,
        nodeedge_color = nodeedgecolor_unweighted,
        edge_color = edgecolor,
        labeldict = labeldict_unweighted,
        node_size_lst = nodesize_unweighted, 
        edge_width_lst = edgesize,
        node_divisor = node_divisor,
        edge_divisor = edge_divisor,
        title = title,
        filename = filename,
        outfolder = outfolder,
        k = k,
        seed = seed,
        nudge_triple = nudge_triple)

    ## weighted degree 
    print('--> generating weighted degree plot')
    node_divisor = 2.5*10.5
    edge_divisor = 100*edge_mult
    title = 'Diplomats and Media sub-network (nodesize: number of neighbors weighted)'
    filename = 'network_focus_weighted_degree'

    plot_network(
        G = G, 
        nodelst = nodelst_weighted,
        edgelst = edgelst,
        color_dct = c_node,
        node_color = nodecolor_weighted,
        nodeedge_color = nodeedgecolor_weighted,
        edge_color = edgecolor,
        labeldict = labeldict_weighted,
        node_size_lst = nodesize_weighted, 
        edge_width_lst = edgesize,
        node_divisor = node_divisor,
        edge_divisor = edge_divisor,
        title = title,
        filename = filename,
        outfolder = outfolder,
        k = k,
        seed = seed,
        nudge_triple = nudge_triple)

    ''' in-degree '''
    print('--> generating in-degree plot')
    node_divisor = 1.5*10
    edge_divisor = 100*edge_mult
    title = 'Diplomats and Media sub-network (nodesize: in-degree -- inwards)'
    filename = 'network_focus_in_degree'

    plot_network(
        G = G, 
        nodelst = nodelst_indegree,
        edgelst = edgelst,
        color_dct = c_node,
        node_color = nodecolor_indegree,
        nodeedge_color = nodeedgecolor_indegree,
        edge_color = edgecolor,
        labeldict = labeldict_indegree,
        node_size_lst = nodesize_indegree, 
        edge_width_lst = edgesize,
        node_divisor = node_divisor,
        edge_divisor = edge_divisor,
        title = title,
        filename = filename,
        outfolder = outfolder,
        k = k,
        seed = seed,
        nudge_triple = nudge_triple)

    ## out-degree
    print('--> generating out-degree plot')
    node_divisor = 1.5*10
    edge_divisor = 100*edge_mult
    title = 'Diplomats and Media sub-network (nodesize: out-degree -- outwards)'
    filename = 'network_focus_out_degree'

    plot_network(
        G = G, 
        nodelst = nodelst_outdegree,
        edgelst = edgelst,
        color_dct = c_node,
        node_color = nodecolor_outdegree,
        nodeedge_color = nodeedgecolor_outdegree,
        edge_color = edgecolor,
        labeldict = labeldict_outdegree,
        node_size_lst = nodesize_outdegree, 
        edge_width_lst = edgesize,
        node_divisor = node_divisor,
        edge_divisor = edge_divisor,
        title = title,
        filename = filename,
        outfolder = outfolder,
        k = k,
        seed = seed,
        nudge_triple = nudge_triple)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-in", "--infile", required=True, help="path to csv")
    ap.add_argument("-out", "--outfolder", required=True, help="path to fig folder")
    ap.add_argument("-n", "--nlabels", required=False, type=int, default=20, help="how many labels on plots")
    args = vars(ap.parse_args())
    main(n_labels = args["nlabels"], infile = args["infile"], outfolder = args["outfolder"])