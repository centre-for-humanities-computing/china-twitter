#!/usr/bin/env bash

# setup 
VENVNAME=cnenv
source /work/cn-some/china-twitter/$VENVNAME/bin/activate
python -m ipykernel install --user --name $VENVNAME --display-name "$VENVNAME"

# run preprocessing
python /work/cn-some/china-twitter/networks/src/code/network_main.py \
	-in  /work/cn-some/china-twitter/networks/data/clean/df_clean.csv \
	-out /work/cn-some/china-twitter/networks/fig/networks \
	-n 20
