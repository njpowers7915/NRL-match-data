from flask import Flask, render_template
from flask_mysqldb import MySQL
import yaml

#create an instance of the Flask class
app = Flask(__name__)

#Configure db
db = yaml.load(open)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

@app.route('/')
def index():
    return render_template('home.html')

#this will allow us to start application
if __name__ == '__main__':
    app.run(debug=True)



# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)
