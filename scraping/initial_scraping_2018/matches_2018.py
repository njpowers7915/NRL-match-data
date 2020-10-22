import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv("DB_USER"),
  passwd=os.getenv("DB_PASSWORD"),
  database="NRL_data"
)
mycursor = mydb.cursor()

#Function to find IDs of values from the database
def find_sql_ids(table_name, identifier, value, mycursor):
    query = """SELECT *
                FROM {table_name}
                WHERE {identifier} = '{value}'
                """
    sql_command = query.format(table_name=table_name, identifier=identifier, value=value)
    #print(sql_command)
    mycursor.execute(sql_command)
    try:
        result = mycursor.fetchone()
        id = result[0]
        return id
    except:
        id = None
        return id

round_url = 'https://en.wikipedia.org/wiki/2017_NRL_season_results'
response = requests.get(round_url)
round_page = BeautifulSoup(response.content, 'html.parser')
round_tables = round_page.find_all('table')

match_list = round_page.find_all('tr', style="text-align:center; background:#f5faff;")

round_dict = {}
round = 1
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
    date = datetime.strptime(unformatted_date, '%A, %d %B, %I:%M %p %Y')

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
    try:
        if score[0].isdigit():
            home_score = score.split(' ')[0]
            away_score = score.split(' ')[-1]
            away_score = away_score.replace('*', '')
        elif ' ' in score[0] == False:
            home_score = score.split('-')[0]
            away_score = score.split('-')[1]
        else:
            home_score = score.split('-')[0]
            away_score = score.split('-')[1]
    except:
        home_score = None
        away_score = None
    print(home_score)
    print(away_score)
    if home_score == None and away_score == None:
        winner = None
        is_draw = None
    elif home_score > away_score:
        winner = home_team_id
        is_draw = 0
    elif home_score < away_score:
        winner = away_team_id
        is_draw = 0
    else:
        winner = None
        is_draw = 1

    #Find Round
    if round in [12, 16]:
        if round in round_dict:
            if round_dict[round] >= 4:
                round += 1
                round_dict[round] = 1
            else:
                round_dict[round] += 1
        else:
            round_dict[round] = 1
    else:
        if round in round_dict:
            if round_dict[round] >= 8:
                round += 1
                round_dict[round] = 1
            else:
                round_dict[round] += 1
        else:
            round_dict[round] = 1

    #Find URL
    mycursor.execute("SELECT nickname FROM Teams WHERE id = %s", (home_team_id,))
    home_team = mycursor.fetchone()[0].lower().strip().replace(' ', '-')
    if home_team == 'tigers':
        home_team = 'wests-tigers'
    mycursor.execute("SELECT nickname FROM Teams WHERE id = %s", (away_team_id,))
    away_team = mycursor.fetchone()[0].lower().strip().replace(' ', '-')
    if away_team == 'tigers':
        away_team = 'wests-tigers'
    url = 'http://www.nrl.com/draw/nrl-premiership/2019/round-' + str(round) + '/' + home_team + '-v-' + away_team + '/'
    matches_2019.append([date, home_team_id, home_score, away_team_id, away_score, winner, is_draw, venue_id, url, round])

#Check data in CSV format
#df = pd.DataFrame(completed_matches, columns=["date", "home_id", "home_score", "away_id", "away_score", "winner", "is_draw", "venue"])
#print(df.to_csv('match_scraping.csv', sep='\t'))

#Add matches to database
for match in matches_2019:
    get_match_url_query = 'SELECT * FROM Matches WHERE url = %s;'
    mycursor.execute(get_match_url_query, (match[8],))
    result = mycursor.fetchall()
    if result != []:
        print('success')
    else:
        print(match)
        insert_match_query ='''INSERT INTO Matches (date, home_team_id, home_score, away_team_id, away_score, winner, is_draw, stadium_id, url, round)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        #mycursor.execute(insert_match_query, (match[0], match[1], match[2], match[3], match[4], match[5], match[6], match[7], match[8], match[9],))
        #mydb.commit()

mydb.close()
