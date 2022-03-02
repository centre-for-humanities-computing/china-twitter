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

''' degree: make smarter '''

def degree_information(G, method, metric):
    '''
    G: <networkx.classes.digraph.DiGraph
    method: G.degree() or variants 
    metric: <str> e.g. "weighted_degree" 
    '''

    degree = {node:val for (node, val) in method}
    nx.set_node_attributes(G, degree, metric)
    degree = nx.get_node_attributes(G, metric).values()
    return degree

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
    lst_sorted = sorted(type_lst, reverse=True)
    cutoff = lst_sorted[n_labels]
    
    # loop over them and assign labels to greater than cutoff 
    labels = nx.get_node_attributes(G, type_str)
    labeldict = {}
    for key, val in labels.items(): 

        if val > cutoff: 
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

#### plot 1 ####
def plot_network(G, color_dct, node_color, edge_color, labeldict, node_size_lst, edge_width_lst, node_divisor, edge_divisor, title, filename, outfolder, seed = 6, nudge_triple = False): 

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
    fig, ax = plt.subplots(figsize=(12, 12), dpi=200, facecolor='w', edgecolor='k')
    plt.axis("off")

    # position & manual tweaking
    pos = nx.spring_layout(G, k=2, iterations=30, seed=seed)
    if nudge_triple: 
        pos = nudge_position(pos, nudge_triple)

    # set up 
    node_size = [x/node_divisor for x in node_size_lst]
    edge_width =  [x/edge_divisor for x in edge_width_lst]

    # draw it 
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color) #, node_size = node_size, node_color = node_color)
    nx.draw_networkx_edges(G, pos, width = edge_width, alpha = 0.5, edge_color = edge_color, arrows=False)

    # labels 
    label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
    nx.draw_networkx_labels(G,pos,labels=labeldict,font_size=12, bbox=label_options)

    # formatting & save
    lines, labels = get_legend(node_size, color_dct)
    fig.legend(lines, labels, title = "Node Category", bbox_to_anchor=(0.2, 0.9), labelspacing=1.2, fontsize=16, title_fontsize=20) # bbox_to_anchor=(0.3, 0.9)
    plt.suptitle(f'{title}', size=25)
    plt.tight_layout()
    plt.savefig(f"{outfolder}/{filename}{seed}.png", bbox_inches='tight')

def main(n_labels, infile, outfolder): 

    ''' setup '''
    print('----- reading data & creating network -----')
    concat = pd.read_csv(f"{infile}") # load data
    concat = concat[concat["mentionee"] != concat['mentioner']] # remove self-mentions
    concat_sub = concat[(concat["category"] == "Media") | (concat['category'] == 'Diplomat')] # only cited by media or diplomat
    weighted_mention = concat_sub.groupby(['mentionee', 'mentioner', 'category', 'category_mentionee']).size().to_frame('weight').reset_index() # weighted
    G = nx.from_pandas_edgelist(weighted_mention,source='mentioner',target='mentionee', edge_attr='weight', create_using=nx.DiGraph()) # create network

    print('----- generating node & edge attributes -----')
    ''' edge attributes '''
    edge_weight = nx.get_edge_attributes(G, 'weight').values()

    ''' node attributes '''
    mentioners = weighted_mention[["mentioner", "category"]].drop_duplicates().rename(columns = {'mentioner': 'node'})
    mentionees = weighted_mention[["mentionee", "category_mentionee"]].drop_duplicates().rename(columns = {'mentionee': 'node', 'category_mentionee': 'category'})
    mentions_category = pd.concat([mentioners, mentionees])
    mentions_category = mentions_category.drop_duplicates()

    # dictionary for category (color)
    mentions_category = dict(zip(mentions_category.node, mentions_category.category))
    nx.set_node_attributes(G, mentions_category, "category")
    category = nx.get_node_attributes(G, 'category').values()
    colors = {'Diplomat': 'tab:blue', 'Media': 'tab:orange'}
    node_color = [colors.get(x) for x in category]

    # size: based on mentions in total dataset. 
    G_nodes = list(G.nodes())
    size_frame = concat.groupby('mentionee').size().to_frame('mentions').reset_index()
    mentionee_size = size_frame[size_frame["mentionee"].isin(G_nodes)]
    mentionee_size_dct = dict(zip(mentionee_size.mentionee, mentionee_size.mentions))
    nx.set_node_attributes(G, mentionee_size_dct, "mentions")
    mentions = nx.get_node_attributes(G, 'mentions').values() # 35- not 40, how?

    unweighted_degree = degree_information(G, G.degree(weight=None), "unweighted_degree")
    weighted_degree = degree_information(G, G.degree(weight='weight'), "weighted_degree")
    in_degree = degree_information(G, G.in_degree(weight='weight'), "in_degree")
    out_degree = degree_information(G, G.out_degree(weight='weight'), "out_degree")
    
    ## run the function (looks good)
    n_labels = args['nlabels'] 
    labeldict_mentions = get_labels(G, 'mentions', mentions, n_labels)
    labeldict_unweighted_degree = get_labels(G, 'unweighted_degree', unweighted_degree, n_labels)
    labeldict_weighted_degree = get_labels(G, 'weighted_degree', weighted_degree, n_labels)
    labeldict_in_degree = get_labels(G, 'in_degree', in_degree, n_labels)
    labeldict_out_degree = get_labels(G, 'out_degree', out_degree, n_labels)

    # edge color 
    for i, j in G.edges():
        i_cat = G.nodes[i]["category"]
        j_cat = G.nodes[j]["category"]

        if i_cat == 'Diplomat' and j_cat == 'Diplomat':
            edge_col = colors.get('Diplomat')
        
        elif i_cat == 'Media' and j_cat == 'Media': 
            edge_col = colors.get('Media')

        else: 
            edge_col = 'tab:grey'

        G[i][j]['color'] = edge_col

    edge_color = nx.get_edge_attributes(G, 'color').values()

    ''' mentions '''
    print('----- generating mentions plot -----')
    node_divisor = 600
    edge_divisor = 100
    title = 'Diplomats and Media sub-network (nodesize: total number of mentions)'
    filename = 'network_focus_mentions'
    nudge_triple = [
        ('MFA_China', 0.05, -0.05), 
        ('ChinaAmbUN', 0, 0.1), 
        #('ChinaAmbGermany', 0.15, 0),
        ('ChineseEmbinUK', 0.05, -0.05),
        ('consulat_de', 0, 0.05),
        ('CHN_UN_NY', -0.05, 0),
        ('ChnMission', 0, 0.05),
        ('ChinaMissionGva', 0, 0.05),
        ('Chinamission2un', 0, 0.05)]

    plot_network(
        G = G, 
        color_dct = colors,
        node_color = node_color,
        edge_color = edge_color,
        labeldict = labeldict_mentions,
        node_size_lst = mentions, 
        edge_width_lst = edge_weight,
        node_divisor = node_divisor,
        edge_divisor = edge_divisor,
        title = title,
        filename = filename,
        outfolder = outfolder,
        #seed = seed,
        nudge_triple = nudge_triple)

    ## unweighted degree
    print('----- generating unweighted degree plot -----')
    node_divisor = 0.05
    edge_divisor = 100
    title = 'Diplomats and Media sub-network (nodesize: number of neighbors)'
    filename = 'network_focus_unweighted_degree'

    plot_network(
        G = G, 
        color_dct = colors,
        node_color = node_color,
        edge_color = edge_color,
        labeldict = labeldict_unweighted_degree,
        node_size_lst = unweighted_degree, 
        edge_width_lst = edge_weight,
        node_divisor = node_divisor,
        edge_divisor = edge_divisor,
        title = title,
        filename = filename,
        outfolder = outfolder,
        nudge_triple = nudge_triple)
        #nudge_triple = nudge_triple)

    ## weighted degree 
    print('----- generating weighted degree plot -----')
    node_divisor = 2.5
    edge_divisor = 100
    title = 'Diplomats and Media sub-network (nodesize: number of neighbors weighted)'
    filename = 'network_focus_weighted_degree'

    plot_network(
        G = G, 
        color_dct = colors,
        node_color = node_color,
        edge_color = edge_color,
        labeldict = labeldict_weighted_degree,
        node_size_lst = weighted_degree, 
        edge_width_lst = edge_weight,
        node_divisor = node_divisor,
        edge_divisor = edge_divisor,
        title = title,
        filename = filename,
        outfolder = outfolder,
        nudge_triple = nudge_triple)
        #nudge_triple = nudge_triple)

    ''' in-degree '''
    print('----- generating in-degree plot -----')
    node_divisor = 1.5
    edge_divisor = 100
    title = 'Diplomats and Media sub-network (nodesize: in-degree -- inwards)'
    filename = 'network_focus_in_degree'

    plot_network(
        G = G, 
        color_dct = colors,
        node_color  =node_color,
        edge_color = edge_color,
        labeldict = labeldict_in_degree,
        node_size_lst = in_degree, 
        edge_width_lst = edge_weight,
        node_divisor = node_divisor,
        edge_divisor = edge_divisor,
        title = title,
        filename = filename,
        outfolder = outfolder,
        nudge_triple = nudge_triple)
        #nudge_triple = nudge_triple)

    ## out-degree
    print('----- generating out-degree plot -----')
    node_divisor = 1.5
    edge_divisor = 100
    title = 'Diplomats and Media sub-network (nodesize: out-degree -- outwards)'
    filename = 'network_focus_out_degree'

    plot_network(
        G = G, 
        color_dct = colors,
        node_color = node_color,
        edge_color = edge_color,
        labeldict = labeldict_out_degree,
        node_size_lst = out_degree, 
        edge_width_lst = edge_weight,
        node_divisor = node_divisor,
        edge_divisor = edge_divisor,
        title = title,
        filename = filename,
        outfolder = outfolder,
        nudge_triple = nudge_triple)
        #nudge_triple = nudge_triple)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-in", "--infile", required=True, help="path to csv")
    ap.add_argument("-out", "--outfolder", required=True, help="path to fig folder")
    ap.add_argument("-n", "--nlabels", required=False, type=int, default=20, help="how many labels on plots")
    args = vars(ap.parse_args())
    main(n_labels = args["nlabels"], infile = args["infile"], outfolder = args["outfolder"])