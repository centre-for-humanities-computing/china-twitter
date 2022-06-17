'''
VMP 2022-05-02: 
try to implement bot detection

NB: OUTDATED
'''

# packages
import pandas as pd 
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

## curate data ## 
### all the files (labeled training data)
fake_followers = "/work/cn-some/china-twitter/bot-detection/datasets_full.csv/fake_followers.csv"
genuine_accounts = "/work/cn-some/china-twitter/bot-detection/datasets_full.csv/genuine_accounts.csv"
social_spambots = [f"/work/cn-some/china-twitter/bot-detection/datasets_full.csv/social_spambots_{i+1}.csv" for i in range(3)]
traditional_spambots = [f"/work/cn-some/china-twitter/bot-detection/datasets_full.csv/traditional_spambots_{i+1}.csv" for i in range(4)]

### gather in list
all_files = []
all_files.append(fake_followers)
all_files.append(genuine_accounts)
all_files += social_spambots
all_files += traditional_spambots

### preprocessing 
def clean_users(file, type): 
    d = pd.read_csv(f"{file}/{type}.csv")
    category = re.search(".csv/(.*).csv", file)[1]
    d = d[["id", "geo_enabled", "verified", "created_at", "followers_count", "friends_count"]]
    d["category"] = category
    d["type"] = type
    return d

d_total = []
for file in all_files: 
    d = clean_users(file, "users")
    d_total.append(d)
    print(f"finished: {file}")
d_complete = pd.concat(d_total)

### assign is_bot category
d_complete['is_bot'] = d_complete['category'].apply(lambda x: 'False' if x == "genuine_accounts" else 'True')

#### fofo ratio ####
d_complete = d_complete.assign(fofo = lambda x: (x["friends_count"]+1)/(x["followers_count"]+1))
d_complete['y'] = [1 if x == 'True' else 0 for x in d_complete['is_bot']]
d_complete.groupby('y').size() # many more bots (might want to balance by sampling & then cross-validation type thing?)

## balance classes ##
class_size = d_complete.groupby('y').size().to_frame(name = 'count').reset_index() # 3474 in non-bot category
min_category = class_size['count'].min()
n_total = 2*min_category # 6948
fraction_bot = 0.5 # reasonable estimate I think???
fraction_human = 1 - fraction_bot 
d_bot = d_complete[d_complete["is_bot"] == "True"].sample(n = np.int(n_total*fraction_bot))
d_hum = d_complete[d_complete["is_bot"] == "False"].sample(n = np.int(n_total*fraction_human))
d_total = pd.concat([d_bot, d_hum])

## simple logistic model
from sklearn.linear_model import LogisticRegression
X = d_total['fofo'].values
y = d_total['y'].values
X = X.reshape(-1, 1)
clf = LogisticRegression(random_state=0).fit(X, y)
print(clf.coef_) # 0.46
print(clf.intercept_) # -0.401
clf.predict_proba([[3.5]]) # higher = more likely to be bot, lower = more likely to be human. 
clf.predict([[3.4]]) # between 3.3 and 3.4

## evaluate on training data 
from sklearn.metrics import accuracy_score
y_pred = clf.predict(X)
accuracy_score(y, y_pred) # accuracy: 0.798 

from sklearn.metrics import confusion_matrix
matrix = confusion_matrix(y, y_pred)
matrix.diagonal()/matrix.sum(axis=1) # mostly true for NOT bot (so.. conservative)

## use it on our data sets (stikprøve) ##
cns = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/CNS1952.csv")
shen = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/shen_shiwei.csv")
ambliu = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/AmbLiuXiaoMing_2007-01-01_2021-02-28.csv")
chiemb = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/ChineseEmbinUK_2007-01-01_2021-02-28.csv")
mfa = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/MFA_China_2007-01-01_2021-02-28.csv")
#zlj_ae = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/MFA_China_2007-01-01_2021-02-28.csv")
#zlj_ak = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/MFA_China_2007-01-01_2021-02-28.csv")
#zlj_an = pd.read_csv("/work/cn-some/china-twitter/bot-detection/mentiondata/MFA_China_2007-01-01_2021-02-28.csv")

## concat zlj
#zlj = pd.concat([zlj_ae, zlj_ak, zlj_an])

## outside test set 
vacc = pd.read_csv("/work/cn-some/china-twitter/bot-detection/vaccination_all_tweets.csv")
vacc = vacc[["user_name", "user_followers", "user_friends"]].rename(
    columns = {
        'user_name': 'mentioner',
        'user_followers': 'followers_mentioner',
        'user_friends': 'following_mentioner'
    }
)

## put them into a list 
lst_df = [cns, shen, ambliu, chiemb, mfa, vacc] # followers_mentioner = followers_count, following_mentioner = friends_count

cols = ["mentioner", "followers_mentioner", "following_mentioner"]
lst_df_clean = []
for i in lst_df: 
    df_clean = i[cols].drop_duplicates()
    lst_df_clean.append(df_clean)

## assign fofo ratio 
lst_fofo = []
for i in lst_df_clean: 
    d_fofo = i.assign(fofo = lambda x: (x["following_mentioner"]+1)/(x['followers_mentioner']+1))
    lst_fofo.append(d_fofo)

## use our predictor
lst_handle = ['cns', 'shen', 'ambliu', 'chiemb', 'mfa', 'vacc']
d_lst = []
for handle, df in zip(lst_handle, lst_fofo): 
    print(handle)
    fofo = df["fofo"].values
    fofo = fofo.reshape(-1, 1)
    y_pred = clf.predict(fofo)
    ## extract bot and human estimate
    pred_human = np.where(y_pred == 0)
    pred_human = pred_human[0].size 
    pred_bot = np.where(y_pred == 1)
    pred_bot = pred_bot[0].size
    ## percent-wise 
    total = pred_human + pred_bot 
    fraction = (total-pred_human)/(total)
    ## gather information
    d_tmp = pd.DataFrame({
        'handle': [handle], 
        'fraction_bot': [fraction],
        'total_human': [pred_human],
        'total_bot': [pred_bot] 
    })
    d_lst.append(d_tmp)

d_total = pd.concat(d_lst)
d_total.head(10)

## get weighted total bots 
our_accounts = ['cns', 'shen', 'ambliu', 'chiemb', 'mfa']
df_subset = d_total[d_total["handle"].isin(our_accounts)]
df_subset = df_subset[['total_human', 'total_bot']].sum().to_frame('sum').reset_index()
total_human = df_subset['sum'][0]
total_bot = df_subset['sum'][1]
total_all = total_human + total_bot
(total_all-total_human)/total_all # 42% overall 