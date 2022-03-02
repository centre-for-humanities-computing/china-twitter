import os
import argparse
import numpy as np
from datetime import date
import matplotlib.pyplot as plt

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from community import community_louvain
from util import bcolors

# tweak this: 
# --> condition perhaps less.

def dist_prune(DELTA, pruning, prune=True):
    """ transform similarity matrix to distance matrix
    - prune matrix by removing edges that have a distance larger
        than condition cond (default mean distance)
    """
    w = np.max(DELTA)
    DELTA = np.abs(DELTA - w)
    #print(f"w: {w}, DELTA: {DELTA}, cond: {np.mean(DELTA)}, std: {np.std(DELTA)}") # inserted. 
    np.fill_diagonal(DELTA, 0.)
    if prune:
        if pruning == "soft":
            cond = np.abs(np.mean(DELTA) + np.std(DELTA))
        elif pruning == "hard":
            cond = np.abs(np.mean(DELTA) - np.std(DELTA))
        else:
            cond = np.mean(DELTA)
        for i in range(DELTA.shape[0]):
            for j in range(DELTA.shape[1]):
                val = DELTA[i, j]
                if val > cond:
                    DELTA[i, j] = 0.
                else:
                    DELTA[i, j] = DELTA[i, j]

    return DELTA


def gen_graph(DELTA, labels, figname="nucleus_graph.png"):
    """ generate graph and plot from DELTA distance matrix
    - labels is list of node labels corresponding to columns/rows in DELTA
    """
    DELTA = DELTA * 10  # scale
    dt = [("len", float)]
    DELTA = DELTA.view(dt)

    #  Graphviz
    G = nx.from_numpy_matrix(DELTA)
    G = nx.relabel_nodes(G, dict(zip(range(len(G.nodes())), labels)))
    pos = graphviz_layout(G)

    G = nx.drawing.nx_agraph.to_agraph(G)

    G.edge_attr.update(color="blue", width="2.0")
    G.node_attr.update(color="red", style="filled")
    G.draw(
        os.path.join("fig", "graph_graphviz.png"),
        format="png", prog="neato"
        )

    G = nx.from_numpy_matrix(DELTA)
    G = nx.relabel_nodes(G, dict(zip(range(len(G.nodes())), labels)))
    nx.draw(G, pos=pos, with_labels=True, node_size=100)
    plt.savefig(os.path.join("fig", "graph_nx.png"))
    plt.close()

    np.random.seed(seed=1234)
    parts = community_louvain.best_partition(G)
    values = [parts.get(node) for node in G.nodes()]

    plt.figure(figsize=(30, 30), dpi=150, facecolor='w', edgecolor='k')
    plt.axis("off")
    nx.draw_networkx(
        G, pos=pos, cmap=plt.get_cmap("Pastel1"), node_color=values,
        node_size=250, font_size=12, width=1, font_weight="bold",
        font_color="k", alpha=1, edge_color="gray"
        )

    plt.tight_layout()
    plt.savefig(figname)
    plt.close()


def main():
    ap = argparse.ArgumentParser(description="[INFO] build graph from nodes and edges")
    ap.add_argument("-s", "--seed", required=True, help="path to seed file")
    ap.add_argument("-t", "--type", required=True, help="paper, abstract or vtt as string")
    ap.add_argument("-a", "--association", required=False, default=False, help="path to set k/m file")
    ap.add_argument("-p", "--pruning", required=False, default=False, help="set pruning file (soft, none, hard)")
    args = vars(ap.parse_args())

    print(f"{bcolors.OKGREEN}[INFO] drawing graph ...{bcolors.ENDC}")
    with open(args["seed"], "r") as fobj:
        seeds = fobj.read().splitlines() 
    
    # read k, m
    if args["association"]: 
        with open(args["association"], "r") as fass: 
            k_m = fass.read().split()
            k, m = map(int, k_m)
    else: 
        k = 3
        m = 10

    if args["pruning"]:
        with open(args["pruning"], "r") as fprun:
            pruning = fprun.read().lower()
    else: 
        pruning = "none"

    delta = np.loadtxt(
        os.path.join("mdl", "edges.dat"), delimiter=","
        )

    DELTA = dist_prune(delta, pruning, prune=True)

    with open(os.path.join("mdl", "nodes.dat"), "r") as f:
        labels = f.read().split("\n")
    labels = labels[:-1]
    
    # new, for different types of data 
    datatype = args["type"]

    outname = os.path.join("fig", f"g_cluster-{'-'.join(seeds).lower()}-{date.today()}-{datatype}-k{k}-m{m}-pruning-{pruning}.png")
    gen_graph(DELTA, labels, figname=outname)

    print(f"{bcolors.OKGREEN}[INFO] writing graph to: {bcolors.ENDC}{bcolors.WARNING}{outname}{bcolors.ENDC}")

if __name__ == '__main__':
    main()

