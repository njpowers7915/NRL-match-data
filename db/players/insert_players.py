#SQL Imports
import mysql.connector
#Pandas imports
import pandas as pd
import numpy as np
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="NYg1@nts",
  database="NRL_data"
)
mycursor = mydb.cursor()

player_data = pd.read_csv('player_info.csv')
player_data = player_data.dropna(subset =['first_name', 'last_name'])
player_data = player_data.replace({pd.np.nan: None})
player_data = player_data.replace(['-'], [None])

i = 0
while i < player_data.shape[0]:
    first_name = player_data.iloc[i]['first_name']
    last_name = player_data.iloc[i]['last_name']
    current_team = player_data.iloc[i]['current_team']
    is_active = True

    try:
        weight_kg = player_data.iloc[i][weight]
        height_cm = player_data.iloc[i][height]
    except:
        weight_kg = None
        height_cm = None

    try:
        date_of_birth = player_data.iloc[i][birth_date]
    except:
        date_of_birth = None

    try:
        city = player_data.iloc[i]['city']
        country = player_data.iloc[i]['country']
    except:
        city = None
        country = None

    try:
        state = player_data.iloc[i]['state']
    except:
        state = None

    player_array = (first_name, last_name, current_team, is_active, weight_kg, height_cm, date_of_birth, city, country, state)
    print(player_array)
    insert_query = ''' INSERT INTO Players (first_name, last_name, current_team, is_active, weight_kg, height_cm, date_of_birth, city, country, state)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    '''
    mycursor.execute(insert_query, player_array)
    mydb.commit()
    i += 1
