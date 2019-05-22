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

#Find and Update Match Formulas
def update_match(id):
    continue

#1. Get URLs that need to be scraped
get_match_url_query = 'SELECT id, url FROM Matches WHERE date > "2018-01-01" AND date < "2018-12-31";'
mycursor.execute(get_match_url_query, )
match_list = mycursor.fetchall()

#2. Set Up WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 10)

#4. Go through all URLs
for match in match_list[:1]:
    match_id = match[0]
    url = match[1]
