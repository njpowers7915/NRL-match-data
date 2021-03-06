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
  passwd="",
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
    find_player_query = 'SELECT id FROM Players WHERE first_name = %s AND last_name LIKE %s AND current_team = %s LIMIT 1;'
    mycursor.execute(find_player_query, (first_name, '%' + last_name + '%', team_id))
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
errors = {'url': []}
match_dictionary = {}
#1. Get URLs that need to be scraped
i = 1
while i <= 8:
    get_match_url_query = 'SELECT id, url FROM Matches WHERE date > "2019-01-01" AND date < "2019-12-31" AND round = ' + str(i) +';'
    mycursor.execute(get_match_url_query, )
    match_list = mycursor.fetchall()
    match_dictionary[i] = match_list
    i += 1

#2. Set Up WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 10)

#4. Go through all URLs
for round in match_dictionary:
    player_match_stats = {}
    for match in match_dictionary[round][1:2]:
        match_id = match[0]
        url = match[1]
        try:
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

            for xpath in [home_xpath_div, away_xpath_div]:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="player-stats"]/div[' + xpath + ']/div/div[3]/div/table/tbody')))

                i = 1
                while i <= 17:
                    name_field = driver.find_element_by_xpath('//*[@id="player-stats"]/div[' + xpath + ']/div/div[3]/div/table/tbody/tr['+ str(i) +']/td[2]/a').get_attribute('innerText').strip()
                    first_name = name_field.split(' ')[0].strip().capitalize()
                    last_name = name_field.split(' ')[-1].strip().capitalize()
                    middle_name = name_field.split(' ')[-2].strip()
                    if middle_name.isalpha():
                        last_name = middle_name.capitalize() + ' ' + last_name
                    if xpath == home_xpath_div:
                        avoid_name_collision = home_team
                        current_team = home_id
                    elif xpath == away_xpath_div:
                        avoid_name_collision = away_team
                        current_team = away_id
                    full_name = first_name + '_' + last_name + '_' + avoid_name_collision
                    player_id = find_or_create_player(first_name, last_name, str(current_team))
                    #print(player_id)
                    #i += 1

                    player_match_stats[full_name] = []
                    player_match_stats[full_name].append(player_id)
                    if xpath == home_xpath_div:
                        player_match_stats[full_name].append(home_id)
                    elif xpath == away_xpath_div:
                        player_match_stats[full_name].append(away_id)
                    player_match_stats[full_name].append(match_id)

                    column = 3
                    while column <= 66:
                        if column in [5, 7, 15, 17, 21, 34, 40, 47, 56, 64]:
                            column += 1
                            continue
                        else:
                            stat_field = driver.find_element_by_xpath('//*[@id="player-stats"]/div[' + xpath + ']/div/div[3]/div/table/tbody/tr[' + str(i) + ']/td[' + str(column) + ']')
                            player_match_stats[full_name].append(stat_field.get_attribute('innerText').strip())
                            column += 1
                    print(player_match_stats[full_name])
                    i += 1
        except:
            errors['url'].append(url)
            print('error with' + url)
            i+= 1

    csv_data = pd.DataFrame.from_dict(player_match_stats, orient='index', columns=column_names).replace('-', 0)

    csv_data = csv_data.replace({pd.np.nan: 0})
        #clean csv_data
    for column in ['conversion_percentage', 'tackle_percentage']:
        csv_data[column] = csv_data[column].str.replace('%', '').astype('float') / 100
        csv_data[column] = csv_data[column].round(3)

    for column in ['minutes_played', 'stint_one', 'stint_two']:
        csv_data[column] = csv_data[column].str.replace(':', '.').astype('float')

    csv_data['average_play_the_ball_seconds'] = csv_data['average_play_the_ball_seconds'].str.replace('s', '').astype('float')
            #csv_data['minutes_played'] = csv_data['minutes_played'].str.replace(':00', '').astype(int)
    csv_data['position_id'] = csv_data['position'].apply(find_position_id)

    print(csv_data)

    #CSV naming
    csv_data.to_csv('round_' + str(round) + '_2019' + '.csv') #index=False)

print(errors)

#NEED TO ADD --> Round 1: Need to add Kinghts vs Sharks


'''
    i = 0
    while i <= 33:
            p = csv_data.iloc[i]

            result_tuple = (p['match_id'].astype('int'),
            p['team_id'].astype('int'),
            p['position_id'].astype('int'),
            p['minutes_played'].astype('float'),
            p['points'].astype('int'),
            p['tries'].astype('int'),
            p['conversions'].astype('int'),
            p['conversion_attempts'].astype('int'),
            p['penalty_goals'].astype('int'),
            p['conversion_percentage'].astype('float'),
            p['field_goals'].astype('int'),
            p['total_runs'].astype('int'),
            p['total_run_metres'].astype('int'),
            p['kick_return_metres'].astype('int'),
            p['post_contact_metres'].astype('int'),
            p['line_breaks'].astype('int'),
            p['line_break_assists'].astype('int'),
            p['try_assists'].astype('int'),
            p['line_engaged_runs'].astype('int'),
            p['tackle_breaks'].astype('int'),
            p['hit_ups'].astype('int'),
            p['play_the_ball'].astype('int'),
            p['average_play_the_ball_seconds'].astype('float'),
            p['dummy_half_runs'].astype('int'),
            p['dummy_half_run_metres'].astype('int'),
            p['steals'].astype('int'),
            p['offloads'].astype('int'),
            p['dummy_passes'].astype('int'),
            p['passes'].astype('int'),
            p['receipts'].astype('int'),
            p['pass_to_run_ratio'].astype('float'),
            p['tackle_percentage'].astype('int'),
            p['tackles_made'].astype('int'),
            p['tackles_missed'].astype('int'),
            p['intercepts'].astype('int'),
            p['kicks_defused'].astype('int'),
            p['kicks'].astype('int'),
            p['kicking_metres'].astype('int'),
            p['forced_drop_outs'].astype('int'),
            p['bomb_kicks'].astype('int'),
            p['grubbers'].astype('int'),
            p['fourty_twenty'].astype('int'),
            p['cross_field_kicks'].astype('int'),
            p['kicked_dead'].astype('int'),
            p['errors'].astype('int'),
            p['handling_errors'].astype('int'),
            p['one_on_ones_lost'].astype('int'),
            p['penalties'].astype('int'),
            p['on_report'].astype('int'),
            p['sin_bins'].astype('int'),
            p['send_offs'].astype('int'),
            p['stint_one'].astype('int'),
            p['stint_two'].astype('int'))
            query = INSERT INTO PlayerMatchStats (match_id, team_id, position_id, minutes_played, points, tries,
            conversions, penalty_goals, conversion_percentage, field_goals, total_runs, total_run_metres,
            kick_return_metres, post_contact_metres, line_breaks, line_break_assists, try_assists,
            line_engaged_runs, tackle_breaks, hit_ups, play_the_ball, average_play_the_ball_seconds,
            dummy_half_runs, dummy_half_run_metres, steals, offloads, dummy_passes, passes, receipts,
            pass_to_run_ratio, tackle_percentage, tackles_made, tackles_missed, incercepts, kicks_defused,
            kicks, kicking_metres, forced_drop_outs, bomb_kicks, grubbers, fourty_twenty, cross_field_kicks,
            kicked_dead, errors, handling_errors, one_on_ones_lost, penalties, on_report, sin_bins, send_offs)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);


            mycursor.execute(query, result_tuple)
            mycursor.commit()
            print('success!')
            i += 1
'''


    #print(name_field)
# <--player 1 stats
#print(player_row)
