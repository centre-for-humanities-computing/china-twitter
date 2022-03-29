"""
usage:
    python chcaa/json2csv_all_from.py --filepath /data/china-mette-thuno/twitter/
"""

# imports 
import ndjson
import datetime, time
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import os
import argparse 
from pathlib import Path
import io



media_list = ["shen_shiwei", "CGTNOfficial", "XHNews", "ChinaDaily", "chenweihua", "CNS1952", "PDChina", "PDChinese", "globaltimesnews", "HuXijin_GT", "XinWen_Ch", "QiushiJournal"]

diplomat_list = ['AmbassadeChine', 'Amb_ChenXu', 'ambcina', 'AmbCuiTiankai', 'AmbLiuXiaoMing','CCGBelfast','ChinaAmbUN','chinacgedi', 'ChinaConsulate', 'ChinaEmbassyUSA','ChinaEmbGermany','ChinaEUMission','ChinaInDenmark','China_Lyon','Chinamission2un','ChinaMissionGva','ChinaMissionVie','chinascio', 'ChineseEmbinUK', 'ChineseEmbinUS', 'ChnMission','CHN_UN_NY', 'consulat_de', 'EUMissionChina','GeneralkonsulDu','MFA_China','SpokespersonCHN', 'SpokespersonHZM','zlj517', 'AmbCina', 'ChinaConSydney', 'ChinaEmbOttawa', 'ChinaCGCalgary', 'ChinaCGMTL', 'ChinainVan', 'ChnEmbassy_jp', 'ChnConsul_osaka']


def subset_dates(df, filter_dates="True"):
    '''
    df: <pd.dataframe>
    subset_dates: <bool> defaults to true 
    ''' 

    df["created_at"] = df["created_at"].astype("datetime64[ns]") 
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.date

    if filter_dates == "True": 
        df = df[
            (df["created_at"] >= datetime.date(2019,11,1)) &
            (df["created_at"] <= datetime.date(2021,2,28))]

    return df

def get_category(string, media_list, diplomat_list):
    if string in media_list:
        return "Media"
    elif string in diplomat_list:
        return "Diplomat"
    else:
        return "Neither"
    
    
def check(tweet_data):
    if tweet_data["text"].encode("utf-8").startswith("RT @"):
        if tweet_data.get('includes'):
            tweetinfo = tweet_data.get('includes')
            if tweetinfo.get('tweets'):
                return True
    else:
        return False

def convert_to_df(data):
    """Converts a ndjson-file to a pd.DataFrame
    Args:
        data (.ndjson): .ndjson-file containing the necessary information
    Returns:
        pd.DataFrame: Dataframe containing the necessary information.
    """    
    dataframe = {
        "username": [row["includes"]["users"][0]["username"] for row in data],
        "tweetID": [row.get('id').encode("utf-8") for row in data],
        "text": [[row['text'] for row in row.get('includes')['tweets']][0].replace('\r','') if check(row) else row["text"].encode("utf-8").replace('\r','') for row in data],
        "lang": [row["lang"] for row in data],
        "created_at": [row["created_at"] for row in data],
        "hashtags": [", ".join([x["tag"] for x in row.get("entities").get("hashtags")]) if row.get("entities") and row.get("entities").get("hashtags") else None for row in data],
        "retweet_count": [row["public_metrics"]["retweet_count"] for row in data],
        "reply_count": [row["public_metrics"]["reply_count"] for row in data],
        "like_count": [row["public_metrics"]["like_count"] for row in data],
        "followers_count": [row["includes"]["users"][0]["public_metrics"]["followers_count"] for row in data],
        "following_count": [row["includes"]["users"][0]["public_metrics"]["following_count"] for row in data],
        "tweet_count": [row["includes"]["users"][0]["public_metrics"]["following_count"] for row in data],
        "listed_count": [row["includes"]["users"][0]["public_metrics"]["listed_count"] for row in data],
        "retweet": [row["referenced_tweets"][0]["type"] if row.get("referenced_tweets") else "original" for row in data]
    }

    return pd.DataFrame(dataframe)

def load_data(data_path):
    """Loads all the ndjson-files in the specified data_path, converts them to a df and concatenates them.

    Args:
        data_path (str): Path to the folder of the ndjson-files.

    Returns:
        pd.DataFrame: Concatenated dataframe of all the files.
    """    
    file_list = os.listdir(data_path)

    file_list = [file for file in file_list if re.match("from", file)]

    dataframes = []

    for i in file_list:
        with open(data_path + i, "r") as file:
            data = ndjson.load(file)
        dataframes.append(convert_to_df(data))
    
    return pd.concat(dataframes, axis = 0).reset_index(drop = True)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-f','--filepath', required=True, help='path to dir with json')
    args = vars(ap.parse_args())

    df = load_data(args['filepath'])
    df = subset_dates(df)
    df["category"] = df["username"].apply(lambda x:get_category(x, media_list, diplomat_list))
    df['tweetID']= df['tweetID'].astype('str')
    df.to_csv('all_from/updated.csv', index = False, encoding =  "utf-8")
