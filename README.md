The code for recreating the analysis for the paper (insert paper title here).

For the purpose of this study data was collected from select twitter accounts, respectively from Chinese diplomacy and Chinese state media propaganda. 

| Handle          | Account type        ||
|:----------------|:--------------------|:------------------------------------------------------------------------|
| @Amb_ChenXu     | Chinese diplomacy   ||
| @AmbassadeChine | Chinese diplomacy   ||
| @AmbCina        | Chinese diplomacy   ||
| @AmbCuiTiankai  | Chinese diplomacy   ||
| @AmbLiuXiaoMing | Chinese diplomacy   ||
| @CCGBelfast     | Chinese diplomacy   ||
| @China_Lyon     | Chinese diplomacy   ||
| @ChinaAmbUN     | Chinese diplomacy   ||
| @chinacgedi     | Chinese diplomacy   ||
| @ChinaConsulate | Chinese diplomacy   ||
| @ChinaEmbGermany| Chinese diplomacy   ||
| @ChinaEUMission | Chinese diplomacy   ||
| @ChinaInDenmark | Chinese diplomacy   ||
| @Chinamission2un| Chinese diplomacy   ||
| @ChinaMissionGva| Chinese diplomacy   ||
| @ChinaMissionVie| Chinese diplomacy   ||
| @chinascio      | Chinese diplomacy   ||
| @ChineseEmbinUK | Chinese diplomacy   ||
| @ChineseEmbinUS | Chinese diplomacy   ||
| @CHN_UN_NY      | Chinese diplomacy   ||
| @ChnMission     | Chinese diplomacy   ||
| @consulat_de    | Chinese diplomacy   ||
| @GeneralkonsulDu| Chinese diplomacy   ||
| @MFA_China      | Chinese diplomacy   ||
| @SpokespersonCHN| Chinese diplomacy   ||
| @SpokespersonHZM| Chinese diplomacy   ||
| @zlj517         | Chinese diplomacy   ||
| @ouzhounews     | Chinese state media ||
| @shen_shiwei    | Chinese state media ||
| @CGTNOfficial   | Chinese state media ||
| @XHNews         | Chinese state media ||
| @ChinaDaily     | Chinese state media ||
| @chenweihua     | Chinese state media ||
| @CNS1952        | Chinese state media ||
| @PDChina        | Chinese state media ||
| @PDChinese      | Chinese state media ||
| @globaltimesnews| Chinese state media ||
| @HuXijin_GT     | Chinese state media ||
| @XinWen_Ch      | Chinese state media ||
| @QiushiJournal  | Chinese state media ||


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


## Semantic kernel
1.  Navigate to the topic model folder
```
cd semantic_kernel
```
2. Prepare data for semantic kernel

3. Train model and generate graphs






