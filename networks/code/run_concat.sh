#!/usr/bin/env bash

# setup 
VENVNAME=cnenv
source ../$VENVNAME/bin/activate
python -m ipykernel install --user --name $VENVNAME --display-name "$VENVNAME"

# run preprocessing (subset dates): main analysis
#python code/concat_files.py \
#	-i ../mention_data/ \
#	-op data/ \
#       -on df_clean.csv \
#	-f True

# run preprocessing (do not subset dates)
python code/concat_files.py \
	-i ../mention_data/ \
	-op data/ \
	-on df_full.csv \
	-f False

