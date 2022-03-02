"""
utility functions
"""
import os

import re
import spacy
import nltk
import logging
import numpy as np

def init_training():
    logging.basicConfig(
        format="%(asctime)s : %(levelname)  s : %(message)s",
        level=logging.INFO
        )
    global nlp
    nlp = spacy.load("en_core_web_sm")


def stringnorm(s, lemmatize=False, casefold=False, rmpat=[]):
    if casefold:
        s = s.lower()
    if rmpat:
        for pat in rmpat:
            s = re.sub(pat, " ", s)
        s = re.sub(" +", " ", s)
    doc = nlp(s)
    if lemmatize:
        tokens = [token.lemma_ for token in doc]
    else:
        tokens = [str(token) for token in doc]
    
    return tokens

def nmax_idx(l, n=1):
    """ indices for n largest values
    """
    return sorted(range(len(l)), key=lambda x: l[x])[-n:]


def nmin_idx(l, n=1):
    """ indices for n smallest values
    """
    return np.argpartition(l, n)


flatten = lambda l: [item for sublist in l for item in sublist]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SentIter:
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in sorted(os.listdir(self.dirname)):
            with open(os.path.join(self.dirname, fname), "r") as f:
                text = f.read()
            for sentence in nltk.sent_tokenize(text):
                tokens = stringnorm(sentence, lemmatize=True, casefold=True, rmpat=[r"\W+"])
                tokens = [token for token in tokens if len(token) > 1]
                
                if len(tokens) > 4:
                    yield tokens