'''
VMP 2022-06-13: scoring

'''

import pandas as pd 
import pickle
from sklearn.linear_model import LogisticRegression

# loads (our data)
dat_overall = pd.read_csv("/work/cn-some/china-twitter/bot-detection/curated_data/overall_data.csv")
dat_media = pd.read_csv("/work/cn-some/china-twitter/bot-detection/curated_data/media_data.csv")
dat_diplomat = pd.read_csv("/work/cn-some/china-twitter/bot-detection/curated_data/diplomat_data.csv")

## loads (baseline)
dat_vacc = pd.read_csv("/work/cn-some/china-twitter/bot-detection/baseline_data/vaccination_all_tweets.csv")
dat_vacc = dat_vacc[["user_name", "user_followers", "user_friends"]].rename(
    columns = {
        'user_name': 'mentioner',
        'user_followers': 'followers_mentioner',
        'user_friends': 'following_mentioner'
    }
)

# groupby mentioner
dat_vacc = dat_vacc.groupby('mentioner')['followers_mentioner', 'following_mentioner'].mean().reset_index()

## load model 
filename = "/work/cn-some/china-twitter/bot-detection/mdl/bot_detect_mdl.sav"
clf = pickle.load(open(filename, 'rb'))

## get overall stuff (NB: 0 = human, 1 = bot)
def score_record(d, clf):
    # prepare prediction
    d = d.assign(fofo = lambda x: (x['following_mentioner']+1)/(x['followers_mentioner']+1))
    fofo = d['fofo'].values
    account = d['mentioner'].values
    fofo_shaped = fofo.reshape(-1, 1)

    # predict stuff 
    y_pred = clf.predict(fofo_shaped)
    y_val = clf.predict_proba(fofo_shaped)

    # create dataframe
    d_probability = pd.DataFrame(y_val, columns = ['proba_human', 'proba_bot'])
    d_prediction = pd.DataFrame(y_pred, columns = ['prediction'])
    d_handle = pd.DataFrame(account, columns = ['handle'])
    d_foforatio = pd.DataFrame(fofo, columns = ['fofo_ratio'])
    d_total = pd.concat([d_probability, d_prediction, d_handle, d_foforatio], axis=1)

    return d_total

# use the function
d_overall = score_record(dat_overall, clf)
d_media = score_record(dat_media, clf)
d_diplomat = score_record(dat_diplomat, clf)
d_vacc = score_record(dat_vacc, clf)

# write stuff
outpath = "/work/cn-some/china-twitter/bot-detection/res/"
d_overall.to_csv(f"{outpath}/results_overall.csv", index = False)
d_media.to_csv(f"{outpath}/results_media.csv", index = False)
d_diplomat.to_csv(f"{outpath}/results_diplomat.csv", index = False)
d_vacc.to_csv(f"{outpath}/results_vaccine_baseline.csv", index = False)


