'''
from /work/cn-some:
python mentions_net/prep/concat_files.py --i mention_data/ --o mentions_net/data/

2022-02-16: ran modified version filtering for dates on new data
'''

# imports 
import pandas as pd 
import numpy as np
import argparse 
# all files 
from os import listdir
from os.path import isfile, join
import datetime

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

def main(inpath, outpath, outname, filter_dates = "True"): # , engine='python', error_bad_lines=False)
    print("--- starting processing ---")
    onlyfiles = [f for f in listdir(inpath) if isfile(join(inpath, f))]
    df_list = [pd.read_csv(f"{inpath}{onlyfile}") for onlyfile in onlyfiles] # Skipping line 556991: unexpected end of data
    df_gathered = pd.concat(df_list)
    df_clean = subset_dates(df_gathered, filter_dates)
    df_clean.to_csv(f"{outpath}{outname}", index = False)
    print("--- finished writing file ---")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inpath", required=True, type=str, help="file to process (csv)")
    ap.add_argument("-op", "--outpath", required=True, type=str, help='path to folder for saving output files (txt)')
    ap.add_argument('-on', "--outname", required=True, type=str, help='filename out')
    ap.add_argument("-f", "--filter_dates", required=False, type=str, default="True", help="subset dates (True) or not (False)")
    args = vars(ap.parse_args())
    main(inpath = args['inpath'], outpath = args['outpath'], outname = args['outname'], filter_dates = args["filter_dates"])