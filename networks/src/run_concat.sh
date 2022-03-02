#!/usr/bin/env bash

# setup 
VENVNAME=cnenv
source /work/cn-some/china-twitter/$VENVNAME/bin/activate
python -m ipykernel install --user --name $VENVNAME --display-name "$VENVNAME"

# run preprocessing (do not subset dates)
python /work/cn-some/china-twitter/networks/src/code/concat_files.py \
	-i work/cn-some/china-twitter/networks/data/raw/ \
	-op work/cn-some/china-twitter/networks/data/clean/ \
	-on df_full.csv \
	-f False

