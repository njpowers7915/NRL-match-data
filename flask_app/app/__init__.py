from flask import Flask

#Initialize the app
app = Flask(__name__, instance_relative_config=True)

#Load views
from app import views

#Load config file
app.config.from_object('config')
