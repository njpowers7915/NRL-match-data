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
from datetime import datetime
from dotenv import load_dotenv
import os

mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv("DB_USER"),
  passwd=os.getenv("DB_PASSWORD"),
  database="NRL_data"
)
mycursor = mydb.cursor()

#1. Get URLs that need to be scraped
get_team_urls = 'SELECT url FROM Teams;'
mycursor.execute(get_team_urls, )
url_list = mycursor.fetchall()

roster_pages = []
for url in url_list:
    page = url[0] + '/teams'
    roster_pages.append(page)

#2. Set Up WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 10)

team_player_urls = ['https://www.bulldogs.com.au/teams/telstra-premiership/canterbury-bankstown-bulldogs/morgan-harper/']

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

player_info_list = []
for player_url in team_player_urls:
    driver.get(player_url)
    player_info = {}
    player_info['is_active'] = True

    current_team_url = player_url.split('/teams/')[0]
    find_team_id = 'SELECT id FROM Teams WHERE url = %s;'
    mycursor.execute(find_team_id, (current_team_url,))
    player_info['current_team'] = mycursor.fetchone()[0]
    try:
        name = driver.find_element_by_xpath('/html/body/div[4]/main/div[1]/div[1]/div[3]/div/div/div/div/div/h1').get_attribute('innerText').strip()
        player_info['first_name'] = name.split(' ')[0].strip()
        if len(name.split(' ')) == 3:
            player_info['last_name'] = name.split(' ')[1] + name.split(' ')[2]
        else:
            player_info['last_name'] = name.split(' ')[1]
    except:
        pass
    try:
        height = driver.find_element_by_xpath('/html/body/div[4]/main/div[1]/div[2]/div/div/div/div/section[1]/div[2]/div/div/div/div[1]/div/dl[1]/dd').get_attribute('innerText').strip()
        player_info['height'] = int(height.split(' ')[0])
    except:
        pass

    try:
        weight = driver.find_element_by_xpath('/html/body/div[4]/main/div[1]/div[2]/div/div/div/div/section[1]/div[2]/div/div/div/div[1]/div/dl[2]/dd').get_attribute('innerText').strip()
        player_info['weight'] = int(weight.split(' ')[0])
    except:
        pass

    try:
        birth_date = driver.find_element_by_xpath('/html/body/div[4]/main/div[1]/div[2]/div/div/div/div/section[1]/div[2]/div/div/div/div[2]/div/dl[1]/dd').get_attribute('innerText').strip()
        player_info['birth_date'] = datetime.strptime(birth_date, '%d %B %Y')
    except:
        pass

    try:
        birthplace = driver.find_element_by_xpath('/html/body/div[4]/main/div[1]/div[2]/div/div/div/div/section[1]/div[2]/div/div/div/div[2]/div/dl[2]/dd').get_attribute('innerText').strip()
        player_info['city'] = birthplace.split(',')[0].strip()
        if birthplace.split(',')[1].strip() in ['NSW', 'QLD', 'TAS', 'NT', 'VIC', 'WA', 'SA', 'NT', 'ACT']:
            player_info['state'] = birthplace.split(',')[1].strip()
            player_info['country'] = 'AUS'
        else:
            player_info['country'] = birthplace.split(',')[1].strip()
    except:
        pass
    player_info_list.append(player_info)

csv_data = pd.DataFrame(player_info_list)
csv_data.to_csv('player_info.csv') #index=False)
