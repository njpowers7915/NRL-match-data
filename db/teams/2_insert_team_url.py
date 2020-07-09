import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="NYg1@nts",
  database="NRL_data"
)
mycursor = mydb.cursor()
mycursor.execute("USE NRL_data;")
mycursor.execute("SELECT nickname FROM Teams;")
teams_list = mycursor.fetchall()
for team in teams_list:
    url_name = team[0].lower().strip().replace(' ', '')
    if url_name in ['storm', 'knights', 'tigers', 'panthers', 'eels']:
        mycursor.execute('SELECT official_name FROM Teams WHERE nickname = %s;', (url_name,))
        city = mycursor.fetchone()[0].lower().strip()
        if city == 'parramatta':
            city = 'parra'
        url_name = city + url_name
    domain = '.com.au'
    if url_name == 'warriors':
        domain = '.kiwi'
    url = 'https://www.' + url_name + domain
    mycursor.execute('UPDATE Teams SET url = %s WHERE nickname = %s;', (url, team[0]))
    mydb.commit()
