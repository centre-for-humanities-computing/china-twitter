import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 

# loads 
inpath = "/work/cn-some/china-twitter/bot-detection/res"
d_diplomat = pd.read_csv(f"{inpath}/results_diplomat.csv")
d_media = pd.read_csv(f"{inpath}/results_media.csv")
d_overall = pd.read_csv(f"{inpath}/results_overall.csv")
d_vaccine = pd.read_csv(f"{inpath}/results_vaccine_baseline.csv")

# summarize 
## function
def summarize_bots(d, handle):
    n_human = (d['prediction'] == 0).sum()
    n_bot = (d['prediction'] == 1).sum()
    total_records = n_human + n_bot 
    fraction_bot = (total_records - n_human)/(total_records)
    d_summary = pd.DataFrame({
        'handle': [handle],
        'fraction_bot': [fraction_bot],
        'total_human': [n_human],
        'total_bot': [n_bot]})
    return d_summary

## generate summary
diplomat_sum = summarize_bots(d_diplomat, "diplomat")
media_sum = summarize_bots(d_media, "media")
overall_sum = summarize_bots(d_overall, "overall")
vaccine_sum = summarize_bots(d_vaccine, "vaccine_baseline")

## concat and save
d_summary = pd.concat([diplomat_sum, media_sum, overall_sum, vaccine_sum])
d_summary.to_csv(f"{inpath}/d_summary.csv", index = False)

# plots (overall vs. vaccine baseline)
def plot_fofo(d1, d2, l1, l2, cut_off, outfolder, outname): 
    # filter based on cutoff
    d1_cutoff = d1[d1["fofo_ratio"] <= cut_off]
    d2_cutoff = d2[d2["fofo_ratio"] <= cut_off]

    # decision boundary
    max_human = d1[d1["prediction"] == 0].max()["fofo_ratio"]
    min_bot = d1[d1["prediction"] == 1].min()["fofo_ratio"]
    decision_boundary = (max_human + min_bot)/2

    # plot 
    fig, ax = plt.subplots(2, constrained_layout = True)

    for num, [d, l] in enumerate(zip([d1_cutoff, d2_cutoff], [l1, l2])): 

        ## plot d1
        sns.kdeplot(
            data = d, 
            x = "fofo_ratio", 
            fill = 'tab:blue',
            ax = ax[num])
        ax[num].vlines(
            x = decision_boundary, 
            ymin = 0, 
            ymax = 0.3, # manually done for now
            colors = "tab:red", 
            linestyles = 'solid', 
            label = 'decision_boundary'
        )
        ax[num].set_title(l)
        if num == 0: 
            ax[0].set_xlabel('')
        if num == 1: 
            ax[1].set_xlabel('fofo ratio (following/followers)')
        ax[num].annotate(
            "Human Acc.", 
            (-1, 0.25)
        )
        ax[num].annotate(
            "Bots & Fake Acc.",
            (4.2, 0.25)
        )

        plt.savefig(f"{outfolder}/{outname}_cutoff{cut_off}.png", bbox_inches='tight')

plot_fofo(
    d1 = d_overall, 
    d2 = d_vaccine, 
    l1 = "Chinese Media and Diplomats",
    l2 = "Vaccine Twitter Baseline",
    cut_off = 20,
    outfolder = "/work/cn-some/china-twitter/bot-detection/res",
    outname = "overall_vs_baseline")