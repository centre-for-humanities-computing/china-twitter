#!/usr/bin/env bash

VENVNAME=semanticenv

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate

pip --version
pip install --upgrade pip
pip --version

#sudo apt-get update allow-releaseinfo-change
#sudo apt-get update --fix-missing
sudo apt-get --allow-releaseinfo-change update
sudo apt-get -y install graphviz graphviz-dev
sudo apt-get -y install zip unzip

# problems when installing from requirements.txt
pip install ipython
pip install jupyter
pip install matplotlib
pip install pygraphviz

python -m ipykernel install --user --name=$VENVNAME

test -f requirements.txt && pip install -r requirements.txt

deactivate
echo "build $VENVNAME"
