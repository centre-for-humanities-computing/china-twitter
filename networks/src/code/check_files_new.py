# imports 
import pandas as pd 
import numpy as np
import datetime, time 

df1 = pd.read_csv("/work/cn-some/mention_data/XHNewse.csv") # PROBLEMATIC
df2 = pd.read_csv("/work/cn-some/mention_data/Amb_ChenXu.csv") # GOOD

def subset_dates(df):
    '''
    df: <pd.dataframe>
    ''' 

    # df["created_at"] = df["created_at"].astype("datetime64[ns]") 
    df["time"] = [x[0:10] for x in df["created_at"]] # same as above
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.date

    df = df[
        (df["created_at"] >= datetime.date(2019,11,1)) &
        (df["created_at"] <= datetime.date(2021,2,28))]

    return df


df1.isna().sum() # A LOT OF NA 
df1_notna = df1.dropna() # DROP NA 

df1_sub = subset_dates(df1) # THIS GIVES ERROR (XHNewse)
df2_sub = subset_dates(df2) # THIS WORKS (Amb_ChenXu)
df1_sub = subset_dates(df1_notna) # THIS WORKS (XHNewse without NA)

sub_dates["created_at"].min()
sub_dates["created_at"].max()

# load 
concat = pd.read_csv("/work/cn-some/mentions_net/data/concat_new.csv")

# check 
concat.dtypes # still float. 

# overall check
len(concat) # 24.953.025
len(concat.drop_duplicates()) # a few duplicates. 
len(concat.mentionee.unique()) # from 71 to 647.
len(concat.mentioner.unique()) # from 566.740 to 3.862.271
concat.retweet.unique() # neither = nan & diplomat??
concat.category.unique() # neither = nan?

# check "category"
concat.groupby('category').size().to_frame('count').reset_index().sort_values('count', ascending=False).head() # almost all "Neither"
concat.groupby('retweet').size().to_frame('count').reset_index().sort_values('count', ascending=False).head() # retweets & reply most often. 

# check whether category is unique 
cat = concat[["mentioner", "category"]]
cat_distinct = cat.drop_duplicates()
len(cat_distinct) # very few. 
len(concat.mentioner.unique()) # unique

# who are duplicated? 
cat_distinct.groupby('mentioner').size().to_frame('count').reset_index().sort_values('count', ascending=False).head(15)

## questions 
### neither = nan?
### category refers to mentionee or mentioner - unique for each mentioner/mentionee?
### any words in "text" that we are interested in?
### retweet, what do we want to use it for?

## check zlj 
concat[(concat["category"] == 'Neither') & (concat["mentionee"] == "zlj517") & (concat["mentioner"] != 'zlj517')]