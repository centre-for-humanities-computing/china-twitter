#!/usr/bin/env bash

# setup 
VENVNAME=cnenv
source /work/cn-some/china-twitter/$VENVNAME/bin/activate
python -m ipykernel install --user --name $VENVNAME --display-name "$VENVNAME"

# what to run
PRE=false
NET=true
SUM=false

# run preprocessing 
if [ $PRE = true ]
then 
	python /work/cn-some/china-twitter/networks/src/concat_files.py \
		-i /work/cn-some/china-twitter/networks/data/raw/ \
		-op /work/cn-some/china-twitter/networks/data/clean/ \
		-on df_rt.csv \
		-f True \
		-or True
fi

# plot networks
if [ $NET = true ]
then
	python /work/cn-some/china-twitter/networks/src/network_main.py \
		-in  /work/cn-some/china-twitter/networks/data/clean/df_rt.csv \
		-out /work/cn-some/china-twitter/networks/fig/networks_rt \
		-n 12
fi 

# summary stats
if [ $SUM = true ]
then
	# summary stats (diplomat/media)
	python /work/cn-some/china-twitter/networks/src/summary_stats_focus.py \
		-in  /work/cn-some/china-twitter/networks/data/clean/df_rt.csv \
		-out /work/cn-some/china-twitter/networks/fig/stats_rt

	# summary stats (global)
	#python /work/cn-some/china-twitter/networks/src/summary_stats.py \
	#	-in  /work/cn-some/china-twitter/networks/data/clean/df_full.csv \
	#	-out /work/cn-some/china-twitter/networks/fig/stats
fi 
