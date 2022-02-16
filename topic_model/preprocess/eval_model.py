import pickle as pkl
from gen_model import LDA_model #load previous function for LDA

with open(f"data/models/GridSearchLDA.pkl", "rb") as f:
    data = pkl.load(f)

## Find best hyperparameters
# media

media = data[(data["Category"] == "Media")]
best_media = media[media["Coherence"] == max(media["Coherence"])]

# diplo

diplo = data[(data["Category"] == "Diplomat")]
best_diplo = diplo[diplo["Coherence"] == max(diplo["Coherence"])]

# english text
with open("data/english_clean.pkl", "rb") as f:
    df = pkl.load(f)
    df = df[df["retweet"] != "retweeted"]

def gen_best_LDA(best_df, df):
    category, topics, alpha, beta, __ = best_df.values[0]
    df_filt = df[df["Category"] == category]
    
    model_dict = LDA_model(
        df = df_filt, 
        filters = (10, 0.5), 
        n = topics,
        beta = beta, 
        alpha = alpha, 
        only_coherence = False)

    
    with open(f"data/models/{category}_LDA.pkl", "wb") as f:
        pkl.dump(model_dict, f)

    print("Model Saved!")
    
if __name__ == "__main__":
    gen_best_LDA(best_media, df)
    gen_best_LDA(best_diplo, df)
