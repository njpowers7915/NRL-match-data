from flask import Flask, request, redirect, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_marshmallow import Marshmallow
import os
#from flask_mysqldb import MySQL
#from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship

#from flask_restful import Resource, Api
#from marshmallow_jsonapi.flask import Schema, ResourceRelationship
#from marshmallow_jsonapi import fields
#import yaml
#from forms import PlayerSearchForm

#Create Flask App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('mysql://root:NYg1%40nts@localhost:3306/NRL_data')
db = engine.connect()
#Database

#Init ma
ma = Marshmallow(app)
'''
# Player Class/Model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column

    def __init__(self, first_name, last_name, current_team):
        self.first_name = first_name
        self.last_name = last_name
        self.current_team = current_team

#Player Schema
class PlayerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'current_team')

#Init Schema
player_schema = PlayerSchema(strict=True)
players_schema = PlayersSchema(many=True, strict=True)
'''
@app.route('/')
def index():
    return render_template('home.html')
    #return jsonify({"about": "Hello!"})



#Get All Players
@app.route('/players', methods=['GET'])
def get_players():
    all_players = Player.query.all()
    result = players_schema.dump(all_players)
    return jsonify(result.data)

# Get Single Player
@app.route('/player/<id>', methods=['GET'])
def get_player(id):
    player = Player.query.get(id)
    return player_schema.jsonify(player)



#api.add_resource(Player, '/')
#api.add_resource(Team, '/multi/<int:num>')




'''
@app.route('/docs')
def docs():
    return render_template('documentation.html')

@app.route('/players', methods=['GET', 'POST'])
def players():
    search = PlayerSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('players.html', form=search)

@app.route('/player_results')
def player_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == '':
        pass




#def player_id():
#    cur = mysql.connection.cursor()
#    cur.execute("SELECT * FROM Players")
#    fetchdata = cur.fetchall()
#    cur.close
#    return render_template('players.html', data=fetchdata)


@app.route('/stat_leaders')
def stat_leaders():
    return('stat_leaders.html')

@app.route('/upcoming_matches')
def upcoming_matches():
    return('upcoming_matches.html')

@app.route('/standings')
def standings():
    return('standings.html')
    #cur = mysql.connection.cursor()
    #cur.execute("SELECT winner FROM Matches WHERE ")

#@app.route('/login')
#def login():
#    return render_template('login.html')

'''
# Run Server
if __name__ == '__main__':
    app.run(debug=True)
