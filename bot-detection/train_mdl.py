'''
VMP 2022-05-02: 
try to implement bot detection
'''

# packages
import pandas as pd 
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

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

# preprocessing 
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
n_total = 2*min_category
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
accuracy_score_overall = accuracy_score(y, y_pred) # accuracy: 0.798 

from sklearn.metrics import confusion_matrix
matrix = confusion_matrix(y, y_pred)
accuracy_per_category = matrix.diagonal()/matrix.sum(axis=1) # mostly true for NOT bot (so.. conservative)

## save model & validation metrics
filename = "/work/cn-some/china-twitter/bot-detection/mdl/bot_detect_mdl.sav"
pickle.dump(clf, open(filename, 'wb'))

accuracy_score_overall
human_accuracy, bot_accuracy = accuracy_per_category

info_log = pd.DataFrame({
    'attribute': ['overall', 'human', 'bot'],
    'accuracy': [accuracy_score_overall, human_accuracy, bot_accuracy]
})

info_log.to_csv("/work/cn-some/china-twitter/bot-detection/mdl/model_info.csv", index = False)





