## Scraping

All of the data contained in this database was scraped from the official [NRL website](https://www.nrl.com/).

When I first began this project, I was only interested in compiling information on one season as I was looking to put together a quick database to practice my analysis skills. I chose 2018 as the season and later used this information to analyse player performance which can be found [here]
(https://github.com/njpowers7915/NRL-match-data/blob/master/analysis_2018/Analysis%20-%202018%20Team%20of%20the%20Year.ipynb).

I later wanted to create an algorithm that predicts match stats so I included data for all matches from 2013 onward.

The Jupyter Notebook 1_insert_match_data_into_db shows how I added match information to the database for all years excluding 2018. The code for 2018 can be found in the file matches_2018.py in the initial_scraping_2018 folder.

Once I had data pertaining to each individual match in my database, I began scraping each individual match URL for individual player stats. The code for this process can be found in the notebooks 2_stat_scraper_2018 and 2_stat_scraper_non-2018.

All of the scraped data was exported to CSV files for validation on my end. Once I spot checked that the information in the CSV files looked correct, I uploaded the CSV files via the code included in the Notebook 3_insert_csv_data.
