#!/usr/bin/env bash

# setup 
VENVNAME=cnenv
source ../$VENVNAME/bin/activate
python -m ipykernel install --user --name $VENVNAME --display-name "$VENVNAME"

# run preprocessing
python /work/cn-some/mentions_net/code/network_main.py \
	-in  /work/cn-some/mentions_net/data/df_clean.csv \
	-out /work/cn-some/mentions_net/fig \
	-n 20
