"""
index for topic importance pr. handle
- writes two files
  1. 'author_topic_px.csv' raw mean probability ($\theta_bar$) per handle
  2. 'author_topic_index.xlsx' index 1: max, 30: min for relative importance of hidden variables pr. author
  
NB: all estimates are stored at dictionaries (for JSON export), but written to 2d files pr. request
"""
import os
import numpy as np
import pandas as pd

def main():
    fname = os.path.join('..','data','diplomats_noretweet_theta_df.csv')
    df = pd.read_csv(fname)
    ii = 20
    colnames = df.columns.values[ii:]
    theta_dict, index_dict = dict(), dict()
    m, n = df.shape
    p_post = list()
    for (i, usr) in enumerate(sorted(list(set(df['username'].values)))):
        idx = df['username'] == usr
        p_post.append(sum(idx)/m*100)
        print(f'[INFO] processing {i}th handle: {usr}...')        
        sub_theta_avg = df.loc[idx, :].iloc[:,ii:].values.mean(axis=0)
        # write to json
        theta_dict[usr] = sub_theta_avg
        # index 1: max, 30: min
        index = np.zeros(sub_theta_avg.shape, dtype=int)
        index[np.argsort(sub_theta_avg)] = range(30,0,-1)
        index_dict[usr] = index

    # write to tabular
    df_px = pd.DataFrame.from_dict(theta_dict, orient='index', columns = colnames)
    df_px['author_presence'] = p_post    
    df_px.to_csv(os.path.join('..', 'data', 'author_topic_px.csv'), index=True)
    df_idx = pd.DataFrame.from_dict(index_dict, orient='index', columns = colnames)
    df_idx['author_presence'] = p_post
    df_idx.to_excel(os.path.join('..', 'data', 'author_topic_index.xlsx'), index=True)
    
if __name__=='__main__':
    main()