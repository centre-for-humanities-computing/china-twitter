'''
VMP 2022-06-13: 
validation on vaccine data set (baseline)
'''

# packages
import pandas as pd 
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

## outside test set 
vacc = pd.read_csv("/work/cn-some/china-twitter/bot-detection/vaccination_all_tweets.csv")
vacc = vacc[["user_name", "user_followers", "user_friends"]].rename(
    columns = {
        'user_name': 'mentioner',
        'user_followers': 'followers_mentioner',
        'user_friends': 'following_mentioner'
    }
)

## load model 
filename = "/work/cn-some/china-twitter/bot-detection/mdl/bot_detect_mdl.sav"
clf = pickle.load(open(filename, 'rb'))

## 
def fofo_scoring(d, handle): 
    d = d.assign(fofo = lambda x: (x["following_mentioner"]+1)/(x["followers_mentioner"]+1))
    fofo = d["fofo"].values
    fofo = fofo.reshape(-1, 1)
    y_pred = clf.predict(fofo)
    pred_human = np.where(y_pred == 0)
    pred_human = pred_human[0].size 
    pred_bot = np.where(y_pred == 1)
    pred_bot = pred_bot[0].size
    ## percent-wise 
    total = pred_human + pred_bot 
    fraction = (total-pred_human)/(total)
    ## gather information
    d = pd.DataFrame({
        'handle': [handle], 
        'fraction_bot': [fraction],
        'total_human': [pred_human],
        'total_bot': [pred_bot] 
    })
    return d 

d_score = fofo_scoring(vacc, "vaccine")

## save 
d_score.to_csv("/work/cn-some/china-twitter/bot-detection/res/baseline_res.csv", index = False)