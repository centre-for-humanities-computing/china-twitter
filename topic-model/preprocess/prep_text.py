from nltk.util import trigrams
import pandas as pd 
import spacy
import re
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
import string
import gensim
import pyLDAvis
import pickle as pkl
import os


def spacy_lemmatize(texts, nlp, **kwargs):
    """Lemmatize texts. 

    Args:
        texts (array/list of lists): Can be provided with for instance running df["text_column"].values
        nlp (spacy.model): Language model from spacy

    Returns:
        list of lists: list of lists containing the lemmas for each word in every list.
    """    
    docs = nlp.pipe(texts, **kwargs)
    def __lemmatize(doc):
        lemmas = []
        for sent in doc.sents:
            for token in sent:
                lemmas.append(token.lemma_)
        return lemmas
    return [__lemmatize(doc) for doc in docs]

def clean_lemmas(lemmas):
    """Clean list of lists of lemmas. Lowers all characters. Removes urls, strings containing only digits, and other stuff.

    Args:
        lemmas (list of lists): Typically the returned list of lists from "spacy_lemmatization"

    Returns:
        list of lists: cleaned list of all lemmas
    """   
    usa = [[x if x not in [' US ', ' usa ', ' USA ', ' United States of America ', ' U.S. ', ' u.s. ', ]  else 'USA' for x in listing] for listing in lemmas]
   
    #to lower
    lemma_to_lower = [[x.lower() for x in listing] for listing in usa]
    
    #remove stopwords
    non_stops = [[x for x in listing if x not in stopwords] for listing in lemma_to_lower]

    #concat corona
    non_corona = [[x if x not in [" corona ", " coronavirus ", " covid-19 ", " covid_19 "] else "covid19" for x in listing] for listing in non_stops]

    #remove punctuation
    puncts_pattern = re.compile(rf"(?<![a-zA-Z])[{string.punctuation}]+(?![a-zA-Z])")
    non_puncts = [[x for x in listing if not re.match(puncts_pattern, x)] for listing in non_corona]

    #remove url
    url_pattern = re.compile(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
    non_urls = [[x for x in listing if not re.match(url_pattern, x)] for listing in non_puncts]

    #remove digits
    digits_pattern = re.compile(r"(?<![a-zA-Z]|.)+[\d]+")
    non_digits = [[x for x in listing if not re.match(digits_pattern, x)] for listing in non_urls]

    #remove plurals
    plural_pattern = re.compile(r"’|'")
    non_plural = [[x for x in listing if not re.match(plural_pattern, x)] for listing in non_digits]
    non_plural = [[x for x in listing if not "'" in x] for listing in non_plural]
    non_plural = [[x for x in listing if not "’" in x] for listing in non_plural]

    #remove new line
    new_line_pattern = re.compile(r"[\n]")
    non_new_line = [[x for x in listing if not re.match(new_line_pattern, x)] for listing in non_plural]

    #remove space
    non_space = [[x for x in listing if x != " " or x != "" or x != "\xa0" or x != "…"] for listing in non_new_line]

    #only length > 1
    non_length = [[x for x in listing if len(x) >= 2] for listing in non_space]
    only_letters_numbers = re.compile(r"[^A-Za-z0-9]+")
    non_others = [[x for x in listing if not re.match(only_letters_numbers, x)] for listing in non_length]

    #only length < 25
    non_length = [[x for x in listing if len(x) < 25] for listing in non_others]

    #remove n't and n`t
    non_nt = [[x for x in listing if x != "n’t" or x != "n't"] for listing in non_length]

    #remove "/"
    non_slash = [[x for x in listing if "/" not in x] for listing in non_nt]
    
    #no tags:
    tags_pattern = re.compile(r"@")
    non_tags = [[x for x in listing if not re.match(tags_pattern, x)] for listing in non_slash]
    non_dots = [[x for x in listing if "." not in x] for listing in non_tags]
    
    #no amp
    non_amp = [[x for x in listing if "amp" not in x] for listing in non_dots]
    
    return non_amp

if __name__ == "__main__":
    #read the data
    df = pd.read_csv('data/all_from.csv')
    #subset the data to only english
    df_eng = df[df["lang"] == "en"] 
    #making sure that we differentiate between US and and us and who and WHO
    df_eng['text'] = df_eng['text'].str.replace(' US ', ' USA ', case = True)
    df_eng['text'] = df_eng['text'].str.replace(' WHO ', ' WorldHealthOrganization ', case = True)
    #load language model
    nlp = spacy.load("en_core_web_sm")
    #set stopwords
    stopwords = set(stopwords.words("english"))
    lemmas = spacy_lemmatize(df_eng["text"].values, nlp)
    texts = clean_lemmas(lemmas)

    ## bigrams and trigrams

    bigram = gensim.models.Phrases(texts)
    texts = [bigram[line] for line in texts]
    trigram = gensim.models.Phrases(texts)
    texts = [trigram[line] for line in texts]

    df_eng["text_clean"] = [" ".join(text) for text in texts]
    df_eng.to_csv('data/all_from_clean.csv')