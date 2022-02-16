Topic modelling using LDA package in python (See documentation:https://lda.readthedocs.io/en/latest/). 


Usage:
1.  Navigate to the topic model folder
```
cd topic_model
```


1. Install requirements
* Pip install
```
pip install -r requirements.txt
```
* Download en_core_web_sm
```
python -m spacy download en_core_web_sm
```

2. Lemmatization and cleaning of tweets
```
python preprocess/prep_text.py
```

3. Generate multiple models with a variety of hyperparameters  
```
python preprocess/gen_model.py
```

4. Evaluate the topic models created above, and determining which is the best one
```
python preprocess/eval_model.py
```

When the model has been generated using above commands, run the code in the topic_model.ipynb to visualize the results.


