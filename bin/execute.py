import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="NYg1@nts",
  database="NRL_data"
)
mycursor = mydb.cursor()
query = input("Enter query: ")
mycursor.execute("CREATE TABLE")
