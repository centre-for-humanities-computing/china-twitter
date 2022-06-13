'''
VMP 2022-05-02
check what data we have.....
NB: OUTDATED
'''

# import stuff
import pandas as pd 
import re
import numpy as np
pd.set_option('display.max_colwidth', None)

# load the data
cns = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/CNS1952.csv")
shen = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/shen_shiwei.csv")
ambliu = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/AmbLiuXiaoMing_2007-01-01_2021-02-28.csv")
chiemb = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/ChineseEmbinUK_2007-01-01_2021-02-28.csv")
mfa = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/MFA_China_2007-01-01_2021-02-28.csv")
zlj_ae = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/MFA_China_2007-01-01_2021-02-28.csv")
zlj_ak = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/MFA_China_2007-01-01_2021-02-28.csv")
zlj_an = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/MFA_China_2007-01-01_2021-02-28.csv")

## concat zlj
zlj = pd.concat([zlj_ae, zlj_ak, zlj_an])

#### try the fofo thing ####
cols = ["mentioner", "followers_mentioner", "following_mentioner"]
cns_fofo = cns[cols].drop_duplicates()
shen_fofo = shen[cols].drop_duplicates()
ambliu_fofo = ambliu[cols].drop_duplicates()
chiemb_fofo = chiemb[cols].drop_duplicates()
mfa_fofo = mfa[cols].drop_duplicates()
zlj_fofo = zlj[cols].drop_duplicates()

def flag_by_fofo(d, cutoff, account_follows, follows_account): 
    d = d.assign(fofo = lambda x: (x[account_follows]+1)/(x[follows_account]+1))
    d["fofo"].median() # close to the same mean as our baseline dataset
    d["issue"] = d['fofo'].apply(lambda x: 1 if x > 5 else 0) 
    #sns.histplot(cns_fofo, x = "fofo", hue = "issue")
    #plt.xlim(0,50)
    d = d.groupby('issue').size().reset_index(name = 'count') # 0: 24.424 vs 1: 23.206
    d['fraction'] = (d['count'] / d['count'].sum()) 
    return d 

## flag them 
c = 5
cns_flagged_5 = flag_by_fofo(cns_fofo, c, "following_mentioner", "followers_mentioner")
shen_flagged_5 = flag_by_fofo(shen_fofo, c, "following_mentioner", "followers_mentioner")
ambliu_flagged_5 = flag_by_fofo(ambliu_fofo, c, "following_mentioner", "followers_mentioner")
chiemb_flagged_5 = flag_by_fofo(chiemb_fofo, c, "following_mentioner", "followers_mentioner")
mfa_flagged_5 = flag_by_fofo(mfa_fofo, c, "following_mentioner", "followers_mentioner")
zlj_flagged_5 = flag_by_fofo(zlj_fofo, c, "following_mentioner", "followers_mentioner")

cns_flagged_5 # 49% bots
shen_flagged_5 # 27% bots
ambliu_flagged_5 # 30%
chiemb_flagged_5 # 21%
mfa_flagged_5 # 31%
zlj_flagged_5 # 31%

# compare to covid
vacc = pd.read_csv("/work/cn-some/china-twitter/bot-detection/vaccination_all_tweets.csv")
vacc = vacc[["user_name", "user_followers", "user_friends"]].drop_duplicates()

vacc_flagged_5 = flag_by_fofo(vacc, 5, "user_followers", "user_friends")
vacc_flagged_5 # 19% bots

vacc_fofo = vacc.assign(fofo = lambda x: (x["user_followers"]+1)/(x["user_friends"]+1))
vacc_fofo["issue"] = vacc_fofo["fofo"].apply(lambda x: 1 if x > 5 else 0)
vacc_fofo.groupby('issue').size() # 0: 110.862 vs. 1: 25.928

## verified we already have 

## profileimg 
test_str = "default_profile_images"
cns["default_img"] = [test_str in str(x) for x in cns["profileimg_mentioner"]]

## popularity
def popularity_metric(friends_count: int, followers_count: int):
    return np.round(np.log(1+friends_count) * np.log(1+followers_count), 3)

def compute_popularity_metric(row):
    return popularity_metric(friends_count=row["followers_mentioner"],
                             followers_count=row["following_mentioner"])

cns["popularity"] = cns.apply(compute_popularity_metric, axis = 1)

## bots more likely to be new 
cns["account_date"] = pd.to_datetime(cns["created_mentioner"])
cns["tweet_date"] = pd.to_datetime(cns["created_at"])
cns["account_tweet_delta"] = cns["tweet_date"] - cns["account_date"]

## assign total score 
cns_grouped = cns[['mentioner', 'verified_mentioner', 'default_img', 'popularity']].drop_duplicates()
median_popularity = cns_grouped["popularity"].median() # 17
cns_grouped["low_popularity"] = cns_grouped['popularity'].apply(lambda x: 1 if x < 10 else 0)
cns_grouped["default_image"] = cns_grouped["default_img"].apply(lambda x: 1 if x == True else 0)
cns_grouped["verified_mentioner"] = cns_grouped["verified_mentioner"].apply(lambda x: 1 if x == False else 0)
cns_grouped = cns_grouped[["mentioner", "verified_mentioner", "low_popularity", "default_image"]]

#### retweets in rapid succession might also be indicative ####
cns_rt = cns[['mentioner', 'mentionee', 'retweet', 'account_tweet_delta']]
cns_rt["seconds"] = [x.seconds for x in cns_rt["account_tweet_delta"]
cns_rt["delta"] = cns_rt.sort_values('seconds').groupby('mentioner')['seconds'].diff().abs()

### create variables ###
min_delta = cns_rt.groupby('mentioner')['delta'].min().reset_index(name = 'min_delta')
mean_delta = cns_rt.groupby('mentioner')['delta'].mean().reset_index(name = 'mean_delta')
total_delta = cns_rt.groupby('mentioner').size().reset_index(name = 'total_tweets')

### gather variables ###
delta = min_delta.merge(mean_delta, on = 'mentioner', how = "inner")
delta = delta.merge(total_delta, on = 'mentioner', how = "inner")

### we can only consider accounts with more than 1 tweet ###
delta["min_delta"].median() # 600 seconds
delta["mean_delta"].median() # 8289 seconds 

### what is a suspicious threshold? ###
threshold_min = 5 # accounts which have short bursts
threshold_mean = 60 # accounts which are only used once probably

delta["low_min"] = delta['min_delta'].apply(lambda x: 1 if x < threshold_min else 0)
delta['low_mean'] = delta["mean_delta"].apply(lambda x: 1 if x < threshold_mean else 0)

### by definition we do not have a problem with "once" tweeters
### select only the relevant columns 
delta = delta[["mentioner", "low_min", "low_mean"]]

###### merge the two ######
total_data = delta.merge(cns_grouped, on = "mentioner", how = "inner")
total_data = total_data.assign(sum = lambda x: x["low_min"] + x["low_mean"] + x["verified_mentioner"] + x["low_popularity"] + x["default_image"])

## plot distribution ##
import matplotlib.pyplot as plt
grouped_sum = total_data.groupby('sum').size().reset_index(name = 'count')
grouped_sum["cum_perc"] = 100*(grouped_sum["count"].cumsum() / grouped_sum["count"].sum())
grouped_sum.head(5) # only 10% has more than two red flags (but how do we verify?)

## which categories "catch" most? ##
total_data["low_min"].mean() # very few
total_data["low_mean"].mean() # very few
total_data["verified_mentioner"].mean() # almost no verified members
total_data["low_popularity"].mean() # 33%
total_data["default_image"].mean() # 10%
