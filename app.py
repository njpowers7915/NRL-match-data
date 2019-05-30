from flask import Flask, render_template

#create an instance of the Flask class
app = Flask(__name__)
#This prevents us from having to reload the server for every update
#app.debug = True

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
