#Scraping Imports
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
#SQL Imports
import mysql.connector
#Pandas imports
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="NYg1@nts",
  database="NRL_data"
)
mycursor = mydb.cursor()

#1. Get URLs that need to be scraped
get_team_urls = 'SELECT url FROM Teams;'
mycursor.execute(get_team_urls, )
url_list = mycursor.fetchall()
for url in url_list[:1]:
    roster_page = requests.get(url[0] + '/teams')
    soup = BeautifulSoup(roster_page.content)
    player_profiles = soup.find_all("a", "card-themed-hero-profile")
    print(player_profiles)

#2. Set Up WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 10)

//*[@id="profile-search-results"]/section[1]/div[2]/div[2]/div/div/a
//*[@id="profile-search-results"]/section[1]/div[2]/div[4]/div/div/a
--> 1 through 18
//*[@id="profile-search-results"]/section[2]/div[2]/div[2]/div/div/a
--> 1 through 14
