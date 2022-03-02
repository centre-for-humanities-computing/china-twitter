"""
v2 build_nucleus
python src/build_kernel.py --model mdl/vectors_expr3.pcl --seed res/seedlist.txt --norm True
"""
import argparse
import os
import pickle
from scipy import spatial
import numpy as np
import pandas as pd

from util import init_training, stringnorm, nmax_idx, flatten, bcolors

# tweak k & m. 

def nodes(seeds, vectors, k=3, m=10):#todo: option to write kernel_types and kernel_tokens to file
    """
    k:  k associations for 1st level
    m: m associations for 2nd level
    """
    lexicon = sorted(vectors.keys())
    # 1st level: kernel_types
    kernel_types = dict()
    for source in seeds:
        if source in lexicon:
            deltas = list()
            for (i, target) in enumerate(lexicon):
                deltas.append(1 - spatial.distance.cosine(vectors[source], vectors[target]))
        else:
            continue
        idxs = nmax_idx(deltas, n=k)
        tokens = [lexicon[idx] for idx in idxs]
        kernel_types[source] = tokens[::-1]
    typelist = list()
    for kernel_type in kernel_types.keys():
        typelist.append(kernel_types[kernel_type])
    typelist = sorted(list(set(flatten(typelist))))
    # 2nd level: kernel_tokens
    kernel_tokens = dict()
    for source in typelist:
        deltas = list()
        for i, target in enumerate(lexicon):
            deltas.append(1 - spatial.distance.cosine(vectors[source], vectors[target]))
        idxs = nmax_idx(deltas, n=m)
        tokens = [lexicon[idx] for idx in idxs]
        kernel_tokens[source] = tokens[::-1]
    #print(kernel_tokens)
    tokenlist = sorted(list(set(flatten(list(kernel_tokens.values())))))

    return (typelist, tokenlist)


def graph(vectors, types, tokens):
    vector_size = len(list(vectors.values())[0])
    X = np.zeros((len(tokens), vector_size))
    for (i, token) in enumerate(tokens):
        X[i, :] = vectors[token]

    delta = np.zeros((X.shape[0], X.shape[0]))
    for i, x in enumerate(X):
        for j, y in enumerate(X):
            delta[i, j] = 1 - spatial.distance.cosine(x, y)
    np.fill_diagonal(delta, 0.)
    # tag labels
    labels = list()
    for token in tokens:
        if token in types:
            labels.append(token.upper())
        else:
            labels.append(token.lower())
    
    return (X, delta, labels)
    

def main():
    ap = argparse.ArgumentParser(description="[INFO] extract associated terms from seeds")
    ap.add_argument("-m", "--model", required=True, help="path to vector file")
    ap.add_argument("-s", "--seed", required=True, help="path to seed file")
    ap.add_argument("-a", "--association", required=False, default=False, help="path to k, m file")
    ap.add_argument("-n", "--norm", required=False, default=False,  type=bool, help="normalize seed list")
    args = vars(ap.parse_args())


    # read seeds
    with open(args["seed"], "r") as fobj:
        seeds = sorted(list(set(fobj.read().split())))


    # read k, m
    if args["association"]: 
        with open(args["association"], "r") as fass: 
            k_m = fass.read().split()
            k, m = map(int, k_m)
    else: 
        k = 3
        m = 10

    ## normalize seeds
    if args["norm"]:
        print(f"{bcolors.OKGREEN}[INFO] normalizing seeds ...{bcolors.ENDC}")
        init_training()
        seeds = stringnorm(" ".join(seeds), lemmatize=True, casefold=True, rmpat=[r"\W+"])
    
    print(f"{bcolors.OKGREEN}[INFO] seeding graphs with: {bcolors.ENDC}{bcolors.WARNING}{', '.join(seeds)}{bcolors.ENDC}")

    # read vectors
    with open(args["model"], "rb") as handle:
        vectors = pickle.load(handle)
    
    (types, tokens) = nodes(seeds, vectors, k=k, m=m)# write kernel dict to ndjson
    (X, delta, labels) = graph(vectors, types, tokens)

    # store results
    ## write query vectors
    # TODO: make as input path with tag for all files
    np.savetxt(
        os.path.join("mdl", "seeded_vectors.dat"), X, delimiter=","
        )
    ## write similarity matrix
    np.savetxt(
        os.path.join("mdl", "edges.dat"), delta, delimiter=","
        )
    ## write labels (1st order are all caps)
    with open(os.path.join("mdl", "nodes.dat"), "w") as f:
        for label in labels:
            f.write("%s\n" % label)

if __name__=="__main__":
    main()