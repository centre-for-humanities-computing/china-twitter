'''
VMP 2022-02-18: 
Is used in the analysis.
Degree of top actors in sub-network (media + diplomats)
Run on df_clean
'''

# imports 
import pandas as pd 
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt
import argparse 
from matplotlib.lines import Line2D

# plot 
def plot_summary(df, id_col, measure_col, n, title, xlab, ylab, outpath, outname): 
    fig, ax = plt.subplots(dpi=150) 
    df_plot = df.assign(norm_measure = lambda x: x[measure_col]/x[measure_col].max()) # max = 1
    df_plot = df_plot.sort_values("norm_measure", ascending=False)
    df_plot = df_plot[[id_col, "norm_measure"]].head(n)
    df_plot.plot.bar(x=id_col, y="norm_measure") 
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.savefig(f"{outpath}/{outname}", bbox_inches="tight")

def main(infile, outpath):

    print(f"--- starting: stats for sub ---")
    print(f"outpath: {outpath}")
    # load 
    concat = pd.read_csv(f"{infile}")

    # no self-citations
    concat = concat[concat["mentionee"] != concat['mentioner']]

    # only media & diplomat
    concat_sub = concat[(concat["category"] == "Media") | (concat['category'] == 'Diplomat')]
    weighted_mention = concat_sub.groupby(['mentionee', 'mentioner', 'category']).size().to_frame('weight').reset_index() 

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

    from functools import reduce
    data_frames = [degree_df, in_degree_df, out_degree_df]
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['id'],how='inner'), data_frames)

    # plot it 
    fig, ax = plt.subplots(dpi=150)
    df_merged = df_merged.sort_values('degree_total', ascending=False)
    df_plot = df_merged[["id", "in_degree", "out_degree"]].head(10)
    df_plot.index = df_plot["id"]
    df_plot.plot.bar(stacked=True)

    lines = [
        Line2D([0], [0], color = 'tab:blue', linewidth = 4),
        Line2D([0], [0], color = 'tab:orange', linewidth = 4)]

    labels = ['In-degree', 'Out-degree'] # in-degree blue, out-degree orange

    plt.legend(lines, labels, frameon = False)
    plt.title('Top 10 degree (sub-network)')
    plt.xlabel('Handle')
    plt.ylabel('Degree')
    plt.savefig(f"{outpath}/summary_focus_degree.png", bbox_inches='tight')

    ''' centrality https://networkx.org/documentation/stable/reference/algorithms/centrality.html '''
    # get metrics
    between_centrality = nx.betweenness_centrality(G) # paths through node. 
    eigen_centrality = nx.eigenvector_centrality_numpy(G, weight='weight') # centrality of neighbors. 
    close_centrality = nx.closeness_centrality(G) # sum of paths to other nodes.

    # to dataframe
    between_df = pd.DataFrame(between_centrality.items(), columns = ['id', 'between'])
    eigen_df = pd.DataFrame(eigen_centrality.items(), columns = ['id', 'eigen'])
    close_df = pd.DataFrame(close_centrality.items(), columns = ['id', 'close'])

    # generate plots
    plot_summary(between_df, "id", "between", 10, "Top 10 nodes betweenness centrality (sub-network)", "Handle", "Betweenness Centrality", outpath, "summary_focus_between.png")
    plot_summary(eigen_df, "id", "eigen", 10, "Top 10 nodes eigenvector centrality (sub-network)", "Handle", "Eigenvector Centrality", outpath, "summary_focus_eigenvector.png")
    plot_summary(close_df, "id", "close", 10, "Top 10 nodes closeness centrality (sub-network)", "Handle", "Closeness Centrality", outpath, "summary_focus_closeness.png")

    print(f"--- finished: stats for sub ---")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-in", "--infile", required=True, type=str, help="file to process (csv)")
    ap.add_argument("-out", "--outpath", required=True, type=str, help='path to folder for saving output files (txt)')
    args = vars(ap.parse_args())
    main(infile = args['infile'], outpath = args['outpath'])