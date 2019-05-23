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
'''
#1. Get URLs that need to be scraped
get_team_urls = 'SELECT url FROM Teams;'
mycursor.execute(get_team_urls, )
url_list = mycursor.fetchall()

roster_pages = []
for url in url_list:
    page = url[0] + '/teams'
    roster_pages.append(page)
'''
#2. Set Up WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 10)
'''
team_player_urls = []
for roster in roster_pages:
    driver.get(roster)
    for player in ['1', '2']:
        i = 1
        while(True):
            try:
                player_profile = driver.find_element_by_xpath('//*[@id="profile-search-results"]/section[' + player +']/div[2]/div[' + str(i) + ']/div/div/a').get_attribute('href')
                print(player_profile)
                team_player_urls.append(player_profile)
                i += 1
            except:
                break
'''

team_player_urls = ['https://www.weststigers.com.au/teams/telstra-premiership/wests-tigers/benji-marshall/'']
for player_url in team_player_urls:
    driver.get(player_url)
    player_info = {}
    player_info['is_active'] = True

    current_team_url = player_url.split('/teams/')[0]
    find_team_id = 'SELECT id FROM Teams WHERE url = %s;'
    mycursor.execute(find_team_id, (current_team_url,))
    player_info['current_team'] = mycursor.fetchone()[0]

    player_info['name'] = driver.find_element_by_xpath('/html/body/div[4]/main/div[1]/div[1]/div[3]/div/div/div/div/div/h1').get_attribute('innerText').strip()
    player_info['height'] = driver.find_element_by_xpath('/html/body/div[4]/main/div[1]/div[2]/div/div/div/div/section[1]/div[2]/div/div/div/div[1]/div/dl[1]/dd').get_attribute('innerText').strip()
    player_info['weight'] = driver.find_element_by_xpath('/html/body/div[4]/main/div[1]/div[2]/div/div/div/div/section[1]/div[2]/div/div/div/div[1]/div/dl[2]/dd').get_attribute('innerText').strip()
    player_info['birth_date'] = driver.find_element_by_xpath('/html/body/div[4]/main/div[1]/div[2]/div/div/div/div/section[1]/div[2]/div/div/div/div[1]/div/dl[4]/dd').get_attribute('innerText').strip()
    player_info['birthplace'] = driver.find_element_by_xpath('/html/body/div[4]/main/div[1]/div[2]/div/div/div/div/section[1]/div[2]/div/div/div/div[1]/div/dl[4]/dd').get_attribute('innerText').strip()
    print(player_info)
'''
    away_team = driver.find_element_by_xpath('//*[@id="vue-match-centre"]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[3]/div[1]/div/p[2]').get_attribute('href').strip()

//*[@id="profile-search-results"]/section[1]/div[2]/div[2]/div/div/a
//*[@id="profile-search-results"]/section[1]/div[2]/div[4]/div/div/a
--> 1 through 18
//*[@id="profile-search-results"]/section[2]/div[2]/div[2]/div/div/a
--> 1 through 14
'''
