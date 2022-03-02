#!/usr/bin/env bash
VENVNAME=semanticenv
source $VENVNAME/bin/activate
python -m ipykernel install --user --name $VENVNAME --display-name "$VENVNAME"
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt
