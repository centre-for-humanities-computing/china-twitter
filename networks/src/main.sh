#!/usr/bin/env bash

# setup 
VENVNAME=cnenv
source /work/cn-some/china-twitter/$VENVNAME/bin/activate
python -m ipykernel install --user --name $VENVNAME --display-name "$VENVNAME"

# run preprocessing 
python /work/cn-some/china-twitter/networks/src/concat_files.py \
	-i work/cn-some/china-twitter/networks/data/raw/ \
	-op work/cn-some/china-twitter/networks/data/clean/ \
	-on df_full.csv \
	-f False

# plot networks
python /work/cn-some/china-twitter/networks/src/network_main.py \
	-in  /work/cn-some/china-twitter/networks/data/clean/df_clean.csv \
	-out /work/cn-some/china-twitter/networks/fig/networks \
	-n 20

# summary stats (diplomat/media)
python /work/cn-some/china-twitter/networks/src/summary_stats_focus.py \
	-in  /work/cn-some/china-twitter/networks/data/clean/df_clean.csv \
	-out /work/cn-some/china-twitter/networks/fig/stats

# summary stats (global)
python /work/cn-some/china-twitter/networks/src/summary_stats.py \
	-in  /work/cn-some/china-twitter/networks/data/clean/df_clean.csv \
	-out /work/cn-some/china-twitter/networks/fig/stats
