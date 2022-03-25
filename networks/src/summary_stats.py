'''
VMP 2022-03-25: 
Analysis basic stats for the whole network (with non-diplomat and non-media)
Not currently used in the paper. 
'''

# imports 
import pandas as pd 
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt
import math
from functools import reduce
import argparse 

def main(infile, outpath): 
    
    print(f"--- starting: statistics for whole network ---")

    # load 
    concat = pd.read_csv(f"{infile}")

    # no self-citations
    concat = concat[concat["mentionee"] != concat['mentioner']]

    # all categories
    weighted_mention = concat.groupby(['mentionee', 'mentioner', 'category']).size().to_frame('weight').reset_index() 

    # actually make a network
    G = nx.from_pandas_edgelist(weighted_mention,source='mentioner',target='mentionee', edge_attr='weight', create_using=nx.DiGraph())

    ### degree ### 
    degrees = {node:val for (node, val) in G.degree(weight='weight')}
    degrees_sorted = {k: v for k, v in sorted(degrees.items(), key=lambda item: item[1], reverse=True)}

    in_degrees = {node:val for (node, val) in G.in_degree(weight='weight')}
    in_degrees_sorted = {k: v for k, v in sorted(in_degrees.items(), key=lambda item: item[1], reverse=True)}

    out_degrees = {node:val for (node, val) in G.out_degree(weight='weight')}
    out_degrees_sorted = {k: v for k, v in sorted(out_degrees.items(), key=lambda item: item[1], reverse=True)}

    degree_df = pd.DataFrame(degrees_sorted.items(), columns=['id', 'degree_total'])
    in_degree_df = pd.DataFrame(in_degrees_sorted.items(), columns = ['id', 'in_degree'])
    out_degree_df = pd.DataFrame(out_degrees_sorted.items(), columns = ['id', 'out_degree'])

    data_frames = [degree_df, in_degree_df, out_degree_df]
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['id'],how='inner'), data_frames)
    df_merged = df_merged.sort_values('degree_total', ascending=False)
    # plot it 
    fig, ax = plt.subplots(dpi=150)
    df_plot = df_merged[["id", "in_degree", "out_degree"]].head(10)
    df_plot.index = df_plot["id"]
    df_plot.plot.bar(stacked=True)
    plt.title('Top 10 degree')
    plt.xlabel('Handle')
    plt.ylabel('Degree')
    plt.savefig(f"{outpath}/summary_degree.png", bbox_inches='tight')

    print(f"--- finished: statistics for whole network ---")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-in", "--infile", required=True, type=str, help="file to process (csv)")
    ap.add_argument("-out", "--outpath", required=True, type=str, help='path to folder for saving output files (txt)')
    args = vars(ap.parse_args())
    main(infile = args['infile'], outpath = args['outpath'])