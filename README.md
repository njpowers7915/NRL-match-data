# NRL Match Database

This project contains a database of detailed match stats from recent seasons of the National
Rugby League of Australia (NRL).  All of this data was scraped from the official NRL website using Selenium and BeautifulSoup and was cleaned using Python and the Pandas library. To my knowledge, this is the first time that detailed match data from the NRL has been consolidated into one single database. I am currently working on a Flask API to make this data more easily accessible.

## Match Predictions

I am using various Machine Learning algorithms from Python's scikit-learn library to create my own algorithm for predicting match outcomes. This ongoing iterative process can be found by accessing the link below:

https://github.com/njpowers7915/NRL-match-data/blob/master/predictions/predictions_notebook.ipynb

## Team of the Year Analysis

I used the data from the 2018 NRL Season to analyze whether or not the selections for
2018's Team of the Year were justified given the players' stats over the course of the season.
Below is a link to this analysis:

https://github.com/njpowers7915/NRL-match-data/blob/master/analysis_2018/Analysis%20-%202018%20Team%20of%20the%20Year.ipynb


## Accessing the data

You can access this data via two methods:

Method 1 -- Download the MySQL database file (NRL_database.sql) from the db folder in this repository

Method 2 (Under Construction) -- Flask API

## Authors

* **Nick Powers**

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## Acknowledgments

* This data was scraped from the official NRL website (https://www.nrl.com/)
