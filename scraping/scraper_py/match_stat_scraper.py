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

column_names = ['player_id', 'team_id', 'match_id',
'number', 'position', 'minutes_played',
'points', 'tries', 'conversions',
'conversion_attempts', 'penalty_goals', 'conversion_percentage',
'field_goals', 'fantasy_points', 'total_runs',
'total_run_metres', 'kick_return_metres', 'post_contact_metres',
'line_breaks', 'line_break_assists', 'try_assists',
'line_engaged_runs', 'tackle_breaks', 'hit_ups',
'play_the_ball', 'average_play_the_ball_seconds', 'dummy_half_runs',
'dummy_half_run_metres', 'steals', 'offloads',
'dummy_passes', 'passes', 'receipts',
'pass_to_run_ratio', 'tackle_percentage', 'tackles_made',
'tackles_missed', 'ineffective_tackles', 'intercepts',
'kicks_defused', 'kicks', 'kicking_metres',
'forced_drop_outs', 'bomb_kicks', 'grubbers',
'fourty_twenty', 'cross_field_kicks', 'kicked_dead',
'errors', 'handling_errors', 'one_on_ones_lost',
'penalties', 'on_report', 'sin_bins',
'send_offs', 'stint_one', 'stint_two'
]


#DB Connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="NYg1@nts",
  database="NRL_data"
)
mycursor = mydb.cursor(buffered=True)

#Find team and player ids
def find_team_id(name):
    find_team_query = 'SELECT id FROM Teams WHERE nickname = %s;'
    mycursor.execute(find_team_query, (name,))
    return mycursor.fetchone()[0]

def find_position_id(name):
    find_position_query = 'SELECT id FROM Positions WHERE position_name = %s;'
    mycursor.execute(find_position_query, (name,))
    return mycursor.fetchone()[0]

def find_or_create_player(first_name, last_name, team_id):
    find_player_query = 'SELECT id FROM Players WHERE first_name = %s AND last_name = %s AND current_team = %s LIMIT 1;'
    mycursor.execute(find_player_query, (first_name, last_name, team_id))
    result = mycursor.fetchone()
    if result is None:
        insert_player_query = 'INSERT INTO Players (first_name, last_name, current_team) VALUES (%s, %s, %s);'
        data = (first_name, last_name, team_id)
        mycursor.execute(insert_player_query, data)
        mydb.commit()
        result = find_or_create_player(first_name, last_name, team_id)
        return result
    else:
        result = result[0]
        return int(result)


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
    driver.get(url)

    home_team = driver.find_element_by_xpath('//*[@id="vue-match-centre"]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/p[2]').get_attribute('innerText').strip()
    away_team = driver.find_element_by_xpath('//*[@id="vue-match-centre"]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[3]/div[1]/div/p[2]').get_attribute('innerText').strip()
    if home_team == 'Wests Tigers':
        home_team = 'Tigers'
    if away_team == 'Wests Tigers':
        away_team = 'Tigers'
    home_id = find_team_id(home_team)
    away_id = find_team_id(away_team)

    home_xpath_div = '1'
    away_xpath_div = '2'

    player_match_stats = {}
    for x-path in [home_xpath_div, away_xpath_div]:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="player-stats"]/div[' + x-path + ']/div/div[3]/div/table/tbody')))

        i = 1
        while i <= 17:
            name_field = driver.find_element_by_xpath('//*[@id="player-stats"]/div[' + x-path + ']/div/div[3]/div/table/tbody/tr['+ str(i) +']/td[2]/a').get_attribute('innerText').strip()
            first_name = name_field.split(' ')[0].strip().capitalize()
            last_name = name_field.split(' ')[-1].strip().capitalize()
            middle_name = name_field.split(' ')[-2].strip()
            if middle_name.isalpha():
                last_name = middle_name.capitalize() + ' ' + last_name
            full_name = first_name + ' ' + last_name
            player_id = find_or_create_player(first_name, last_name, str(home_id))
            #print(player_id)
            #i += 1

            player_stats[full_name] = []
            player_stats[full_name].append(player_id)
            if x-path == home_xpath_div
                player_stats[full_name].append(home_id)
            elif x-path = away_xpath_div
                player_stats[full_name].append(away_id)
            player_stats[full_name].append(match_id)

            column = 3
            while column <= 66:
                if column in [5, 7, 15, 17, 21, 34, 40, 47, 56, 64]:
                    column += 1
                    continue
                else:
                    stat_field = driver.find_element_by_xpath('//*[@id="player-stats"]/div[' + x-path + ']/div/div[3]/div/table/tbody/tr[' + str(i) + ']/td[' + str(column) + ']')
                    player_stats[full_name].append(stat_field.get_attribute('innerText').strip())
                    column += 1
            i += 1

    csv_data = pd.DataFrame.from_dict(player_match_stats, orient='index', columns=column_names).replace('-', 0)

        #clean csv_data
        for column in ['conversion_percentage', 'tackle_percentage']:
            csv_data[column] = csv_data[column].str.replace('%', '').astype(float) / 100

        for column in ['minutes_played', 'stint_one', 'stint_two']:
            csv_data[column] = csv_data[column].str.replace(':00', '').astype(int)

        csv_data['average_play_the_ball_seconds'] = csv_data['average_play_the_ball_seconds'].str.replace('s', '').astype(float)
        #csv_data['minutes_played'] = csv_data['minutes_played'].str.replace(':00', '').astype(int)
        csv_data['position_id'] = find_position_id(csv_data['position'])

        #add columns so everything is ready to be added to database

        print(csv_data)

    #CSV naming
    csv_identifiers = url.split('/')
    csv_name = '_'.join([csv_identifiers[-4], csv_identifiers[-3], csv_identifiers[-2]])
    csv_data.to_csv(csv_name + '.csv', names=column_names, header=None)


    #print(name_field)
# <--player 1 stats
#print(player_row)
'''
