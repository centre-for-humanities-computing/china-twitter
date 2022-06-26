## Bot detection pipeline. 

### preparation
(1) download "cresci-2017" data from https://botometer.osome.iu.edu/bot-repository/datasets.html
(2) unzip everything into datasets_full.csv folder
(3) download baseline dataset into baseline_data/vaccination_all_tweets.csv (https://www.kaggle.com/datasets/gpreda/all-covid19-vaccines-tweets)

### pipeline
(1) prepare our own data (prepare_fofo_data.py)
(2) train model (train_mdl.py)
(3) score records of our data and basline (scoring.py)
(4) generate summary stats and plots (plots_and_summary.py)