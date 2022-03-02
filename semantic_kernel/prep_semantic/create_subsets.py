'''
Just checking the cleaned data
'''

import pandas as pd 

# subsets 
# no NA 
df = pd.read_csv("../data/all_from_clean.csv")
df.dropna(inplace=True)

# add unique column 
df['ID'] = range(1, len(df.index)+1)

# only english 
df = df[df["lang"] == "en"]

# rename column (important for msg_decomp.py)
df = df.rename(columns={'text_clean': 'Text'})

# select columns ID and text_clean 
df_text_all = df[['ID', 'Text']]
df_text_all.to_csv("../data/text_all.csv", index=False)

# all orig 
df_text_all_orig = df[df["retweet"] == "original"]
df_text_all_orig = df[["ID", "Text"]]
df_text_all_orig.to_csv("../data/text_all_orig.csv", index=False)

# only diplomats 
df_text_diplomat = df[df["category"] == "Diplomat"]
df_text_diplomat = df_text_diplomat[["ID", "Text"]]
df_text_diplomat.to_csv("../data/text_diplomat.csv", index=False)

# only diplomat original 
df_text_diplomat_orig = df[(df["retweet"] == "original") & (df["category"] == "Diplomat")]
df_text_diplomat_orig = df_text_diplomat_orig[["ID", "Text"]]
df_text_diplomat_orig.to_csv("../data/text_diplomat_orig.csv", index=False)

