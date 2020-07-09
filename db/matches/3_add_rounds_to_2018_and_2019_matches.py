import mysql.connector
import datetime as dt
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
mycursor.execute("SELECT id, date FROM Matches;")
match_list = mycursor.fetchall()

rounds_dict_2018 = {}
rounds_dict_2019 = {}
round = 1
round_2019 = 1
for match in match_list:
    match_id = match[0]
    date = match[1]
    if date < dt.date(2018, 5, 28):
        if round in rounds_dict_2018:
            rounds_dict_2018[round].append(match_id)
        else:
            rounds_dict_2018[round] = [match_id]
        if len(rounds_dict_2018[round]) >= 8:
            round += 1
    elif date > dt.date(2018, 5, 29) and date < dt.date(2018, 6, 4):
        round = 13
        if round in rounds_dict_2018:
            rounds_dict_2018[round].append(match_id)
        else:
            rounds_dict_2018[round] = [match_id]
        if len(rounds_dict_2018[13]) >= 4:
            round += 1
    elif date > dt.date(2018, 6, 5) and date < dt.date(2018, 7, 2):
        if round in rounds_dict_2018:
            rounds_dict_2018[round].append(match_id)
        else:
            rounds_dict_2018[round] = [match_id]
        if len(rounds_dict_2018[round]) >= 8:
            round += 1
    elif date > dt.date(2018, 7, 3) and date < dt.date(2018, 7, 9):
        round = 17
        if round in rounds_dict_2018:
            rounds_dict_2018[round].append(match_id)
        else:
            rounds_dict_2018[round] = [match_id]
        if len(rounds_dict_2018[17]) >= 4:
            round += 1
    elif date > dt.date(2018, 7, 11) and date < dt.date(2018, 12, 31):
        if round in rounds_dict_2018:
            rounds_dict_2018[round].append(match_id)
        else:
            rounds_dict_2018[round] = [match_id]
        if len(rounds_dict_2018[round]) >= 8:
            round += 1
    else:
        if round_2019 in rounds_dict_2019:
            rounds_dict_2019[round_2019].append(match_id)
        else:
            rounds_dict_2019[round_2019] = [match_id]
        if len(rounds_dict_2019[round_2019]) >= 8:
            round_2019 += 1
#print(rounds_dict_2018)
#print(rounds_dict_2019)

#insert rounds 2018
for round in rounds_dict_2018:
    for match in rounds_dict_2018[round]:
        mycursor.execute('UPDATE Matches SET round = %s WHERE id = %s;', (round, match))
        mydb.commit()

#insert rounds 2019
for round in rounds_dict_2019:
    for match in rounds_dict_2019[round]:
        mycursor.execute('UPDATE Matches SET round = %s WHERE id = %s;', (round, match))
        mydb.commit()
