from flask import Flask
flaskApp = Flask(__name__)
from onlinextract.api import extractorAPI
from onlinextract.app import views
