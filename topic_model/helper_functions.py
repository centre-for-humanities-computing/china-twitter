import pandas as pd 
import pickle as pkl 
import altair as alt
import numpy as np 

# setting up matplotlib settings
# Source: https://towardsdatascience.com/making-matplotlib-beautiful-by-default-d0d41e3534fd
import matplotlib.pyplot as plt
import seaborn as sns 
import matplotlib.font_manager as font_manager
import pickle as pkl
import pyLDAvis.gensim as gm

#%matplotlib inline
from pandas.plotting import scatter_matrix
import seaborn as sns
sns.set(style="whitegrid")
import re
import pyLDAvis
from tqdm import tqdm

#### Imports
import pandas as pd 
import pickle as pkl 
import altair as alt
import numpy as np 

# setting up matplotlib settings
# Source: https://towardsdatascience.com/making-matplotlib-beautiful-by-default-d0d41e3534fd
import matplotlib.pyplot as plt
import seaborn as sns 
import matplotlib.font_manager as font_manager

import re
import pyLDAvis




# Find the topic number with the highest 
def dominant_topic(ldamodel, corpus, document, save_name = ""):
    '''
    Creates a dataframe, which indicates the dominant topic
    of a given document. 
    ___
    Examples:
    ___
    df_dominant = dominant_topic(models[model_name], corpus, df["org_text"])
    '''
    # init dataframe
    topics_df = pd.DataFrame()

    # GET MAIN TOPIC IN EACH DOCUMENT
    # Get through the pages
    for num, doc in enumerate(tqdm(ldamodel[corpus])):
        # Count number of list into a list
        if sum(isinstance(i, list) for i in doc)>0:
            doc = doc[0]

        doc = sorted(doc, key= lambda x: (x[1]), reverse=True)
    
        for j, (topic_num, prop_topic) in enumerate(doc):
            if j == 0: # => dominant topic
                # Get list prob. * keywords from the topic
                pk = ldamodel.show_topic(topic_num)
                topic_keywords = ', '.join([word for word, prop in pk])
                # Add topic number, probability, keywords and original text to the dataframe
                topics_df = topics_df.append(pd.Series([int(topic_num), np.round(prop_topic, 4),
                                                    topic_keywords, document[num]]),
                                                    ignore_index=True)
            else:
                break
                
    # Add columns name
    topics_df.columns = ['Dominant_Topic', 'Topic_Perc_Contribution', 'Keywords', 'Text']

    if save_name:
        with open(f"data/dominant_dfs/{save_name}.pkl", "wb") as f: 
            pkl.dump(topics_df, f)

    return topics_df

def load_dominant_dfs():
    with open(f"data/dominant_dfs/diplo_dominant.pkl", "rb") as f: 
        diplo = pkl.load(f)
        
    with open(f"data/dominant_dfs/media_dominant.pkl", "rb") as f: 
        media = pkl.load(f)
    
    return diplo, media

def topic_threshold(df, topic, threshold):
    '''
    Creates a subset of the data, which is documents that 
    have a topic_perc_contribution over a set threshold.
    '''
    return df[(df["Dominant_Topic"] == topic) & (df["Topic_Perc_Contribution"] > threshold)].sort_values("Topic_Perc_Contribution", ascending = False)

def query_topic(data, sub_size, query, topic = False):
    '''
    Queries a dataframe and gives a subset of sub_size length.
    This query contains both the topic and a query string. 
    Alternatively, setting topic = False only queries the dataframe
    and returns the sorted dataframe.
    '''
    if topic:
        data = data[(data["Text"].str.contains(query)) & (data["Dominant_Topic"] == topic)]
    else:
        data = data[data["Text"].str.contains(query)]
    return data.sort_values("Topic_Perc_Contribution", ascending=False).head(sub_size)


def topic_names(models, k): 
    """Function for going through all topics and labelling them

    Args:
        models (LDA Model): Topic Model
        k (int): Number of topics to go through

    Returns:
        list: list containing the labels for each topic
    """    

    liste = [] 

    for i in range(k): 
        (models.print_topic(i, 10))
        label = input("Topic Label: ")
        liste.append(label)
        print(liste)

    return liste



def load_models():
    with open("data/models/Media_LDA.pkl", "rb") as f:
        media = pkl.load(f)
    
    with open("data/models/Diplomat_LDA.pkl", "rb") as f:
        diplo = pkl.load(f)
        
    return media, diplo

def visualize_model(dictionary, sort_topics = False):
    #Creating Topic Distance Visualization 
    pyLDAvis.enable_notebook()
    p = gm.prepare(dictionary["model"], dictionary["corpus"], dictionary["id2word"], sort_topics = sort_topics)
    return p