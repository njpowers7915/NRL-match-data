# NRL Match Database

This project is a database of detailed match stats from the current (2019) and recent NRL seasons.
All of this data was scraped from the NRL website using Selenium and BeautifulSoup. To my knowledge,
this is the first time that detailed match data from the NRL has been consolidated into one single
database. I am currently working on a Flask API to make this data more easily accessible.  


## Getting Started

You can access this data via two methods:

Method 1 -- Download the MySQL database file from the db folder in this repository

Method 2 (Under Construction)
  1. Clone the repository

    $ git clone https://github.com/njpowers7915/NRL-match-data

  2. Navigate into the flask_app folder

    $ cd flask_app

  3. Run Flask to access the API

    $ flask run

## Prerequisites

Make sure you have the latest version of Flask installed on your computer


## Authors

* **Nick Powers**

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## Acknowledgments

* This data was scraped from the official NRL website (https://www.nrl.com/)
