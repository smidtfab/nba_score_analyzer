# NBA Score Analyzer
[![Issues !](https://img.shields.io/github/issues/smidtfab/nba_score_analyzer)](https://github.com/smidtfab/nba_score_analyzer/issues)<br>
A full stack application based on python and mongodb to scrape game data from [https://stats.nba.com/](https://stats.nba.com/) and build a continuous predictor.
## Development Setup

First, clone repo if you haven't already and navigate into project directory e.g. Documents/nba_score_analyzer:

  ```bash
  $ cd Documents/nba_score_analyzer
  ```
  
Initialize and activate a virtualenv:
  ```bash
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```
  
Install requirements:
```python
pip install -r requirements.txt
```

## Running the scripts
### Scrape game data and store it in MongoDB:

Either run script with one argument to scrape a specific date:
  ```python
  python3 nba_scraper.py 02/27/2020
  ```

Or run script with two arguments to scrape games that fall in a specific interval:
  ```python
  python3 nba_scraper.py 02/12/2020 02/27/2020
  ```

The scraper will then access the endpoint and scrape the response with the formatting pictured below and store the json in as a document in the MongoDB database.  
Response Header             |  Response Body
:-------------------------:|:-------------------------:
![](https://i.imgur.com/cZwuKZc.png)  |  ![](https://i.imgur.com/K325brF.png)

### Predictor Notebook:
As of now everything concerning the prediction is located in the notebook called predictor.ipynb. The goal is to predict the winner of a future game given the features derived from past games. Therefore, I have fitted the following classifier:

- XGBClassifier
- SVC
- Logistic Regression

## References
### Scraping
- [For play by play](https://nycdatascience.com/blog/student-works/scraping-nba-play-by-play-data-with-scrapy-mongodb/)

- [General static scraper](https://towardsdatascience.com/web-scraping-nba-stats-4b4f8c525994)

### Prediction

- [Logistic Regression Classifier](https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8)

- [Paper on prediction of game outcome](https://www.researchgate.net/publication/312236952_Predicting_the_Outcome_of_NBA_Playoffs_Based_on_the_Maximum_Entropy_Principle)

- [Player stats from inteval](https://fansided.com/2015/10/26/nylon-calculus-101-creating-sportvu-game-logs-in-python/)

- [Continual Learning](https://arxiv.org/pdf/1910.02718.pdf)
