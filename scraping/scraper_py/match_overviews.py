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


matches_2019 = []
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
        home_score = None
        away_score = None
    if home_score > away_score:
        winner = home_team_id
        is_draw = 0
    elif home_score < away_score:
        winner = away_team_id
        is_draw = 0
    elif home_score == None and away_score == None:
        winner = None
        is_draw = None
    else:
        winner = None
        is_draw = 1

    #Find URL
    mycursor.execute("SELECT nickname FROM Teams WHERE id = %s", (home_team_id,))
    home_team = mycursor.fetchone()[0].lower().strip().replace(' ', '-')
    if home_team == 'tigers':
        home_team = 'wests-tigers'
    mycursor.execute("SELECT nickname FROM Teams WHERE id = %s", (away_team_id,))
    away_team = mycursor.fetchone()[0].lower().strip().replace(' ', '-')
    if away_team == 'tigers':
        away_team = 'wests-tigers'
    url = 'http://www.nrl.com/draw/nrl-premiership/' + str(year) + '/round-' + str(round) + '/' + home_team + '-v-' + away_team + '/'
    print(url)
    matches_2019.append([date, home_team_id, home_score, away_team_id, away_score, winner, is_draw, venue_id, url])

#Check data in CSV format
#df = pd.DataFrame(completed_matches, columns=["date", "home_id", "home_score", "away_id", "away_score", "winner", "is_draw", "venue"])
#print(df.to_csv('match_scraping.csv', sep='\t'))

'''
#Add matches to database
for match in matches_2019:
    get_match_url_query = 'SELECT * FROM Matches WHERE url = %s;'
    try:
        mycursor.execute(get_match_url_query, match[8])
        match = mycursor.fetchall()
    except:
        insert_match_query =INSERT INTO Matches (date, home_team_id, home_score, away_team_id, away_score, winner, is_draw, stadium_id, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        mycursor.execute(match_query, (match[0], match[1], match[2], match[3], match[4], match[5], match[6], match[7], match[8]))
        mydb.commit()
'''
