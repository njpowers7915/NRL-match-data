import mysql.connector
from dotenv import load_dotenv
import os

mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv("DB_USER"),
  passwd=os.getenv("DB_PASSWORD"),
  database="NRL_data"
)

mycursor = mydb.cursor()
mycursor.execute("USE NRL_data;")
mycursor.execute("SELECT id, date, round, home_team_id, away_team_id FROM Matches;")
match_list = mycursor.fetchall()
for match_data in match_list:
    id = match_data[0]
    year = match_data[1].year
    round = match_data[2]
    home_team_id = match_data[3]
    away_team_id = match_data[4]
    mycursor.execute("SELECT nickname FROM Teams WHERE id = %s", (home_team_id,))
    home_team = mycursor.fetchone()[0].lower().strip().replace(' ', '-')
    if home_team == 'tigers':
        home_team = 'wests-tigers'
    mycursor.execute("SELECT nickname FROM Teams WHERE id = %s", (away_team_id,))
    away_team = mycursor.fetchone()[0].lower().strip().replace(' ', '-')
    if away_team == 'tigers':
        away_team = 'wests-tigers'
    if year == 2018:
        v = '-vs-'
    else:
        v = '-v-'
    url = 'http://www.nrl.com/draw/nrl-premiership/' + str(year) + '/round-' + str(round) + '/' + home_team + v + away_team + '/'

    mycursor.execute('UPDATE Matches SET url = %s WHERE id = %s;', (url, id))
    mydb.commit()
    #print(url)
