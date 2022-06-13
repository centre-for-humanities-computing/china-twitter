'''
VMP 2022-06-13: scoring

'''

import pandas as pd 

# loads 
dat_overall = pd.read_csv("/work/cn-some/china-twitter/bot-detection/curated_data/overall_data.csv")
dat_media = pd.read_csv("/work/cn-some/china-twitter/bot-detection/curated_data/media_data.csv")
dat_diplomat = pd.read_csv("/work/cn-some/china-twitter/bot-detection/curated_data/diplomat_data.csv")

## load model 
filename = "/work/cn-some/china-twitter/bot-detection/mdl/bot_detect_mdl.sav"
clf = pickle.load(open(filename, 'rb'))

## fun
def fofo_scoring(d, handle): 
    d = d.assign(fofo = lambda x: (x["following_mentioner"]+1)/(x["followers_mentioner"]+1))
    fofo = d["fofo"].values
    fofo = fofo.reshape(-1, 1)
    y_pred = clf.predict(fofo)
    pred_human = np.where(y_pred == 0)
    pred_human = pred_human[0].size 
    pred_bot = np.where(y_pred == 1)
    pred_bot = pred_bot[0].size
    ## percent-wise 
    total = pred_human + pred_bot 
    fraction = (total-pred_human)/(total)
    ## gather information
    d = pd.DataFrame({
        'handle': [handle], 
        'fraction_bot': [fraction],
        'total_human': [pred_human],
        'total_bot': [pred_bot] 
    })
    return d 

# run function
d_overall = fofo_scoring(dat_overall, "overall")
d_media = fofo_scoring(dat_media, "media")
d_diplomat = fofo_scoring(dat_diplomat, "diplomat")

# concat
d_total = pd.concat([d_overall, d_media, d_diplomat])

## save 
d_total.to_csv("/work/cn-some/china-twitter/bot-detection/res/bot_detection_res.csv", index = False)