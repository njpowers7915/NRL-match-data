from flask import Flask, render_template
from flask_mysqldb import MySQL
import yaml
from forms import PlayerSearchForm

#create an instance of the Flask class
app = Flask(__name__)
#mysql = MySQL()

#Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/docs')
def docs():
    return render_template('documentation.html')

@app.route('/players')


@app.route('/players/<player_id>')
def players():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Players")
    fetchdata = cur.fetchall()
    cur.close
    return render_template('players.html', data=fetchdata)

@app.route('/stat_leaders')
def stat_leaders():
    return('stat_leaders.html')

@app.route('/upcoming_matches')
def upcoming_matches():
    return('upcoming_matches.html')

@app.route('/standings')
def standings():
    pass
    #cur = mysql.connection.cursor()
    #cur.execute("SELECT winner FROM Matches WHERE ")

#@app.route('/login')
#def login():
#    return render_template('login.html')


#this will allow us to start application
if __name__ == '__main__':
    app.run(debug=True)
