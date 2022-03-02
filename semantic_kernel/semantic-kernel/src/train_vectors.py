"""
v2 of train_embedding
"""
import argparse

import pickle

import gensim
import logging

from util import bcolors
from util import init_training
from util import stringnorm
from util import SentIter

# tmp
import time

def main(input_dir, mdl_outpath, vectors_outpath):
    start = time.time()

    init_training()
    print(f"{bcolors.OKGREEN}[INFO] preparing data ...{bcolors.ENDC}")
    sentences = SentIter(input_dir)

    print(f"{bcolors.OKGREEN}[INFO] initiating model ...{bcolors.ENDC}")
    mdl = gensim.models.Word2Vec(vector_size=50, window=5, min_count=10, workers=8)# update vector size
    mdl.build_vocab(sentences)
    mdl.train(sentences, total_examples=mdl.corpus_count, epochs=mdl.epochs)# update epochs

    if mdl_outpath:
        mdl.save(mdl_outpath)

    print(f"{bcolors.OKGREEN}[INFO] writing vectors to disc ...{bcolors.ENDC}")
    lexicon = list(mdl.wv.index_to_key)

    db = dict()
    for word in lexicon: 
        #db[word] = mdl.wv[word]
        # alternate options
        db[word] = mdl.wv.get_vector(word)
        #db[word] = model.wv.word_vec(word, use_norm=False)
    
    with open(vectors_outpath, 'wb') as handle:
        pickle.dump(db, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print(f"{bcolors.OKGREEN}[INFO] saved {len(lexicon)} vectors to {vectors_outpath}{bcolors.ENDC}")

    print(f"\n[INFO] runtime {time.time()-start} seconds.")


if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input_dir", required=True, type=str, help="path to folder with X")
    ap.add_argument("-vo", "--vectors_outpath", required=True, type=str, help='dump vectors here (.pcl)')
    ap.add_argument("-mo", "--mdl_outpath", required=False, type=str, help="dump w2v model here (.pcl)")
    args = vars(ap.parse_args())

    main(
        input_dir=args['input_dir'],
        mdl_outpath=args['mdl_outpath'],
        vectors_outpath=args['vectors_outpath']
    )