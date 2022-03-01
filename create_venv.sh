#!/usr/bin/env bash

VENVNAME=cnenv

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate

pip --version
pip install --upgrade pip
pip --version

sudo apt-get --allow-releaseinfo-change update
sudo apt-get -y install graphviz graphviz-dev
sudo apt-get -y install zip unzip
#sudo apt-get -y install python3-graph-tool

sudo apt-get install python3-pil tesseract-ocr libtesseract-dev tesseract-ocr-eng tesseract-ocr-script-latn
sudo apt-get install tesseract-ocr tesseract-ocr-dev
sudo apt-get install libtesseract-dev

# problems when installing from requirements.txt
pip install ipython
pip install jupyter
pip install matplotlib
pip install pytesseract

python -m ipykernel install --user --name=$VENVNAME

test -f requirements.txt && pip install -r requirements.txt

deactivate
echo "build $VENVNAME"
