import ndjson
import pandas as pd
import os
import pickle as pkl
import re

### Setups for loading:
data_path = "/data/china-mette-thuno/twitter/"

file_list = os.listdir(data_path)

file_list = [file for file in file_list if re.match("from", file)]

def convert_to_df(data):
    """Converts a ndjson-file to a pd.DataFrame

    Args:
        data (.ndjson): .ndjson-file containing the necessary information

    Returns:
        pd.DataFrame: Dataframe containing the necessary information.
    """    

    dataframe = {
        "username": ["@"+row["includes"]["users"][0]["username"] for row in data],
        "author_id": [row["author_id"] for row in data],
        "conversation_id": [row["conversation_id"] for row in data],
        "text": [row["text"] for row in data], 
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

### FILTERING BY DATE:

def filter_date(df, year, month, day):
    """Filter the dataframe for dates. Uses pandas.to_datetime as format

    Args:
        df (pd.DataFrame): Dataframe that you want to filter
        year (str): Year of your lower limit
        month (str): Month of your lower limit
        day (str): Day of your lower limit

    Returns:
        pd.DataFrame: pd.DataFrame containing only the entries after the specified time
    """    
    df["created_at"] = pd.to_datetime(df["created_at"])
    test_time = pd.to_datetime(f"{year}-{month}-{day}T00:00:00.000Z")
    return df[df["created_at"] >= test_time].reset_index(drop = True)

### MAKE CATEGORY COLUMN:
def get_category(string, media_list):
    if string in media_list:
        return "Media"
    else:
        return "Diplomat"

### MEDIA LIST FROM GOOGLE DOCS
media_list = ["@ouzhounews", "@shen_shiwei", "@CGTNOfficial", "@XHNews", "@ChinaDaily", "@chenweihua", "@CNS1952", "@PDChina", "@PDChinese", "@globaltimesnews", "@HuXijin_GT", "@XinWen_Ch", "@QiushiJournal"]

if __name__ == "__main__":
    df = load_data(data_path)
    df = filter_date(df, "2019", "11", "01")
    df["Category"] = df["username"].apply(lambda x:get_category(x, media_list))
    with open("../data/2019-11-01_CT.pkl", "wb") as file:
        pkl.dump(df, file)
