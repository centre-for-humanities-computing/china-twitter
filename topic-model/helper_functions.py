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
#import pyLDAvis.gensim as gm

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

#%matplotlib inline
from pandas.plotting import scatter_matrix
import seaborn as sns
sns.set(style="whitegrid")
import re
import pyLDAvis

import matplotlib.dates as mdates
import matplotlib.pyplot as plt


# font
font_dirs = ['/Library/Fonts', ]
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)

plt.rcParams['font.family'] = 'DIN Condensed Bold'

# set matplotlib aesthetics
CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'
CB91_Amber = '#F5B14C'

color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
              CB91_Purple, CB91_Violet]

plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

sns.set(rc={
            'axes.axisbelow': False,
            'axes.edgecolor': 'lightgrey',
            'axes.facecolor': 'None',
            'axes.grid': False,
            'axes.labelcolor': 'dimgrey',
            'axes.spines.right': False,
            'axes.spines.top': False,
            'figure.facecolor': 'white',
            'lines.solid_capstyle': 'round',
            'patch.edgecolor': 'w',
            'patch.force_edgecolor': True,
            'text.color': 'dimgrey',
            'xtick.bottom': False,
            'xtick.color': 'dimgrey',
            'xtick.direction': 'out',
            'xtick.top': False,
            'ytick.color': 'dimgrey',
            'ytick.direction': 'out',
            'ytick.left': False,
            'ytick.right': False,
            'savefig.dpi': 800})

#plt.rcParams["savefig.dpi"] = 'figure'
sns.set_context("notebook", rc={"font.size":12,
                                "axes.titlesize":16,
                                "axes.labelsize":16})


#alt.data_transformers.disable_max_rows()

### MAKE FUNCTIONS

def prep_data():
    """Preparing the data

    Returns:
        pd.Dataframes: Returns three dataframes - the whole dataset, the diplomats and the media.
    """    
    en_df = pd.read_csv("data/all_from_clean.csv")

    en_df['month'] = pd.DatetimeIndex(en_df['created_at']).month
    en_df['date'] = pd.DatetimeIndex(en_df['created_at']).date
    
    
    def retweet_binary(string):
        if string == "retweeted":
            return "Retweet"
        else:
            return "Other"

    en_df["retweet_bin"] = en_df["retweet"].apply(lambda x: retweet_binary(x))
    
    en_df["date"] = pd.to_datetime(en_df["date"])
    
    return en_df, en_df[en_df["category"] == "Diplomat"].reset_index(drop=True), en_df[en_df["category"] == "Media"].reset_index(drop=True)
    
def available_users(data):
    """Function for listing the available users.

    Args:
        data (pd.DataFrame): Data for which the user wants a list of users to use for "options".

    Returns:
        list: list of usernames from the data
    """    
    return list(set(data["username"]))

def tweet_count_plot(data, options):
    """Plots the tweet counts

    Args:
        data (pd.DataFrame): data for plotting
        options (list): subset of the users

    Returns:
        altair plot: Tweet counts over time
    """    
    
    date_freq = pd.DataFrame(data.groupby(['date', 'month', "username"])['created_at'].count()).reset_index()

    date_freq = date_freq.rename(columns = {"date": "Date", "created_at": "Tweet Count", "username": "Username"}, inplace = False)
    
    date_freq = date_freq[date_freq["Username"].isin(options)]
    
    #date_freq["Date"] = pd.to_datetime(date_freq["Date"])
    
    return alt.Chart(date_freq).mark_line().encode(
        x='Date',
        y='Tweet Count',
        color = 'Username',
        tooltip = ["Date", "Tweet Count", "Username"]
    ).properties(
        width=700,
        height=300
    )


def tweet_count_plot_categories(data):
    """Plots the aggregated tweet counts across both categories

    Args:
        data (pd.DataFrame): data for plotting (should contain both categories)

    Returns:
        altair plot: plots of tweets over time for both categories
    """    
    date_freq = pd.DataFrame(data.groupby(['date', 'month', "category"])['created_at'].count()).reset_index()

    date_freq = date_freq.rename(columns = {"date": "Date", "created_at": "Tweet Count"}, inplace = False)

    return alt.Chart(date_freq).mark_line().encode(
        x='Date',
        y='Tweet Count',
        color = 'category',
        tooltip = ["Date", "Tweet Count", "category"]
    ).properties(
        width=700,
        height=300
    )


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

def plot_retweets(en_df):

    en_df['month'] = pd.DatetimeIndex(en_df['created_at']).month
    en_df['date'] = pd.DatetimeIndex(en_df['created_at']).date

    ### OVERALL:

    date_freq = pd.DataFrame(en_df.groupby(['date', 'month', "Category", "retweet_bin"])['created_at'].count()).reset_index()

    date_freq = date_freq.rename(columns = {"date": "Date", "created_at": "Tweets", "retweet_bin": "Retweet"}, inplace = False)

    date_freq["Date"] = pd.to_datetime(date_freq.Date)

    return alt.Chart(date_freq).mark_line().encode(
            x='Date',
            y='Tweets',
            color = 'Retweet',
            tooltip = ["Date", "Tweets", "Category", "Retweet"]
        ).properties(
            width=600,
            height=300
        ).facet(
            row = "Retweet",
            column="Category"
        ).resolve_scale(y='independent')


def plot_retweets_options(en_df, options):
    date_freq = pd.DataFrame(en_df.groupby(['date', 'month', "Category", "username", "retweet_bin"])['created_at'].count()).reset_index()

    date_freq = date_freq.rename(columns = {"date": "Date", "created_at": "Tweets", "retweet_bin": "Retweet"}, inplace = False)

    date_freq["Date"] = pd.to_datetime(date_freq.Date)

    ## filter using options

    #diplomats

    date_freq_diplo = date_freq[date_freq["username"].isin(options)]

    return alt.Chart(date_freq_diplo).mark_line().encode(
            x='Date',
            y='Tweets',
            color = 'username',
            tooltip = ["Date", "Tweets", "Retweet", "username"]
        ).properties(
            width=600,
            height=300
        ).facet(
            row = "Retweet",
        ).resolve_scale(y='independent')
  
    
def plot_bars_retweets(en_df, options):
    date_freq = pd.DataFrame(en_df.groupby(["category", "username", "retweet_bin"])['created_at'].count()).reset_index()

    date_freq = date_freq.rename(columns = {"created_at": "Tweets", "retweet_bin": "Retweet"}, inplace = False)

    ## filter using options

    #diplomats

    date_freq_diplo = date_freq[date_freq["username"].isin(options)]

    return alt.Chart(date_freq_diplo).mark_bar().encode(
            alt.X('Retweet', axis = None),
            y='Tweets',
            color = 'Retweet',
            tooltip = ["Tweets", "Retweet", "username"],
            column = "username"
        ).properties(
            width=alt.Step(40),
            height=300
        )


def get_subset(data, account):
    return data[data["username"] == account]

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

def topics_over_time(lda, data):
    # code adapted from https://jeriwieringa.com/2017/06/21/Calculating-and-Visualizing-Topic-Significance-over-Time-Part-1/
    pyLDAvis.enable_notebook()
    
    distribution = []
    for i in range(len(lda['corpus'])):
        distribution.append(lda['model'][lda['corpus']][i])
        
    no_retweets = data[data["retweet"] != "retweeted"].reset_index(drop = True)
    no_retweets = no_retweets[["text", "created_at"]]
    
    probs = lda['model'].get_document_topics(lda['corpus'], minimum_probability=0, minimum_phi_value=None, per_word_topics=False)

    probsdf = pd.DataFrame(probs)


    for i in range(probsdf.shape[0]):
        for n in range(probsdf.shape[1]):
            probsdf.loc[i, n] = probsdf.loc[i, n][1]
            
    probsdf = probsdf.apply(pd.to_numeric)
    probsdf['topic_weight'] = probsdf.max(axis=1)
    probsdf['topic_id'] = probsdf.idxmax(axis=1)
    
    tweetsandprobs = pd.concat([no_retweets, probsdf], axis=1, join="inner")
    
    # Getting the month and year of each post
    tweetsandprobs['month'] = pd.DatetimeIndex(tweetsandprobs['created_at']).month.astype('str')
    tweetsandprobs['year'] = pd.DatetimeIndex(tweetsandprobs['created_at']).year.astype('str')
    tweetsandprobs['month_year'] = tweetsandprobs['month'] +'_'+  tweetsandprobs['year']
    
    tweetsandprobs = tweetsandprobs.drop(columns=['month', 'year', 'topic_weight', 'topic_id'])
    tweetsandprobs = tweetsandprobs.melt(id_vars =['month_year', 'text', 'created_at'], var_name='topic_id', value_name='topic_weight')
    
    # Grouping by each month in each year to get the total docs column
    total_docs = tweetsandprobs.groupby('month_year')['text'].apply(lambda x: len(x.unique())).reset_index()
    total_docs.columns = ['month_year', 'total_docs']
    
    # Group by year and topic id
    df_avg = tweetsandprobs.groupby(['month_year', 'topic_id']).agg({'topic_weight': 'sum'}).reset_index()
    df_avg = df_avg.merge(total_docs, on="month_year", how="left")
    df_avg['average_weight'] = df_avg['topic_weight'] / df_avg['total_docs']
    
    # renaming for the plot
    df_avg['month_year'] = df_avg['month_year'].replace({
    '11_2019':'Nov 19',
    '12_2019':'Dec 19',
    '1_2020':'Jan 20',
    '2_2020':'Feb 20', 
    '3_2020':'Mar 20', 
    '4_2020':'Apr 20',
    '5_2020':'May 20',
    '6_2020':'Jun 20',
    '7_2020':'Jul 20', 
    '8_2020':'Aug 20', 
    '9_2020':'Sep 20', 
    '10_2020':'Oct 20',
    '11_2020':'Nov 20',
    '12_2020':'Dec 20',
    '1_2021':'Jan 21', 
    '2_2021':'Feb 21'})
    


    
    df_avg['time'] = pd.to_datetime(df_avg['month_year'], format = '%b %y')
    df_avg['topic_id'] = df_avg['topic_id']+1
    
    return df_avg


    
    
    
    
    
    
    
    
    
    
    
    
    