import pandas as pd 
d = pd.read_csv("/work/cn-some/china-twitter/networks/data/clean/df_full.csv")
d2 = pd.read_csv("/work/cn-some/china-twitter/networks/data/clean/rt_df_full.csv")

print(f"length d: {len(d)}") # 26.321.014 total
print(f"length d2: {len(d2)}") # 16.095.732 total 
print(f"length d only RT: {len(d[d['retweet'] == 'retweeted'])}") # 16.095.732 (good)