# china-some
The code for recreating the analysis for the paper (insert paper title here).

## Topic model
Latent Dirichlet Allocation topic modelling using LDA package in python (See documentation:https://lda.readthedocs.io/en/latest/). 
LDA is a hierarchical Bayesian model with three levels, in which each item of a collection, in this case tweets, is modeled as a finite mixture over an underlying set of topics. In turn, each topic is modeled as an infinite mixture over an underlying set of topic probabilities. An explicit representation of each tweet is provided by the topic probabilities. 

Usage:
1.  Navigate to the topic model folder
```
cd topic_model
```

2. Install requirements
* Pip install
```
pip install -r requirements.txt
```
* Download en_core_web_sm
```
python -m spacy download en_core_web_sm
```

3. Lemmatization and cleaning of tweets
```
python preprocess/prep_text.py
```

4. Generate multiple models with a variety of hyperparameters  
```
python preprocess/gen_model.py
```

5. Evaluate the topic models created above, and determining which is the best one
```
python preprocess/eval_model.py
```

When the model has been generated using above commands, run the code in the topic_model.ipynb to visualize the results.


