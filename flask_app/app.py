from flask import Flask
from flask_mysqldb import MySQLdb
from app import app
import yaml

#create an instance of the Flask class
#app = Flask(__name__)

#this will allow us to start application
if __name__ == '__main__':
    app.run(debug=True)

#Configure db
db = yaml.load(open)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)
