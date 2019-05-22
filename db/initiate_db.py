import mysql.connector

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  passwd='NYg1@nts'
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE NRL_data;")

mycursor.close()
