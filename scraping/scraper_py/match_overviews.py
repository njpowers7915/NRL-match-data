import requests
from scraping_queries import find_sql_ids
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="NYg1@nts",
  database="NRL_data"
)
mycursor = mydb.cursor()


round_url = 'https://en.wikipedia.org/wiki/2019_NRL_season_results'
response = requests.get(round_url)
round_page = BeautifulSoup(response.content, 'html.parser')
round_tables = round_page.find_all('table')

match_list = round_page.find_all('tr', style="text-align:center; background:#f5faff;")


completed_matches = []
for match in match_list:
    match_details = match.find_all('td')

    #home team id
    home_team = match_details[0].text.strip().split(' ')[-1]
    if home_team == 'Eagles':
        home_team = 'Sea Eagles'
    home_team_id = find_sql_ids('Teams', 'nickname', home_team, mycursor)

    #away team id
    away_team = match_details[2].text.strip().split(' ')[-1]
    if away_team == 'Eagles':
        away_team = 'Sea Eagles'
    away_team_id = find_sql_ids('Teams', 'nickname', away_team, mycursor)

    #date
    unformatted_date = match_details[3].text.strip() + ' 2019'
    date = datetime.strptime(unformatted_date, '%A, %d %B, %I:%M%p %Y')

    #venue info
    venue = match_details[4].text.strip()
    venue_id = find_sql_ids('Stadiums', 'name', venue, mycursor)
    if venue_id == None:
        insert_stadium_query = 'INSERT INTO Stadiums (name) VALUES (%s);'
        mycursor.execute(insert_stadium_query, (venue,))
        mydb.commit()
    venue_id = find_sql_ids('Stadiums', 'name', venue, mycursor)

    #score info
    score = match_details[1].text.strip()
    if score[0].isdigit():
        home_score = score.split(' ')[0]
        away_score = score.split(' ')[-1]
        away_score = away_score.replace('*', '')
    else:
        continue
    if home_score > away_score:
        winner = home_team_id
        is_draw = 0
    elif home_score < away_score:
        winner = away_team_id
        is_draw = 0
    else:
        winner = None
        is_draw = 1

    completed_matches.append([date, home_team_id, home_score, away_team_id, away_score, winner, is_draw, venue_id])

#Check data in CSV format
#df = pd.DataFrame(completed_matches, columns=["date", "home_id", "home_score", "away_id", "away_score", "winner", "is_draw", "venue"])
#print(df.to_csv('match_scraping.csv', sep='\t'))


#Add matches to database
for match in completed_matches:
    match_query ='''INSERT INTO Matches (date, home_team_id, home_score, away_team_id, away_score, winner, is_draw, stadium_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    mycursor.execute(match_query, (match[0], match[1], match[2], match[3], match[4], match[5], match[6], match[7]))
    mydb.commit()
