'''
Created on Feb 18, 2014

@author: svattam
'''
from onlinextract.app import flaskApp
#from src.api import extractorAPI

@flaskApp.route('/')
@flaskApp.route('/index')
def index():
    return flaskApp.send_static_file('index.html')