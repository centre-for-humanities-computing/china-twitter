# packages
import pandas as pd 
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



d = pd.read_csv("/work/cn-some/china-twitter/bot-detection/datasets_full.csv/genuine_accounts.csv/tweets.csv",  encoding = "ISO-8859-1")
d.dtypes
d_users = pd.read_csv("/work/cn-some/china-twitter/bot-detection/datasets_full.csv/genuine_accounts.csv/users.csv")
d_users.head(5)

vaccine = pd.read_csv("/work/cn-some/china-twitter/bot-detection/vaccination_all_tweets.csv")
vaccine.head(5)
len(vaccine[['user_name']].drop_duplicates())
vaccine["date"].max()
vaccine["date"].min()