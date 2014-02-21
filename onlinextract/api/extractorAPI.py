'''
Created on Feb 18, 2014

@author: svattam
'''
from onlinextract.app import flaskApp
from onlinextract.lib import extractorLib
from flask_restful import reqparse, Resource, Api
import sys

api = Api(flaskApp)
parser = reqparse.RequestParser()
parser.add_argument('url', type=str)

class Extraction(Resource):
    
    #curl http://localhost:5000/extractions/<extID>
    def get(self, extID): # gets an extraction
        ext = extractorLib.Extraction.getExtraction(extID)
        if (ext == None) or (ext == {}):
            return 404 # resource not found
        else:
            return ext, 200 # success
        
    #curl http://localhost:5000/extractions/<extID> -d "url=http://www.gatech.edu" -X PUT -v 
    def put(self, extID): # updates an extraction
        args = parser.parse_args()
        url = args['url']
        if (url == None) or (url == ''):
            return 400 # bad request
        ext = extractorLib.Extraction.updateExtraction(extID, url)
        if (ext == None) or (ext == {}):
            return 404 # resource not found
        else:
            return ext, 200 # success
        
    # curl http://localhost:5000/extractions/<extID> -X DELETE -v
    def delete(self, extID): # deletes an extraction
        ext = extractorLib.Extraction.deleteExtraction(extID)
        if (ext == None) or (ext == {}):
            return 404 # resource not found
        else:
            return ext, 200 # success
        
class ExtractionList(Resource):
    #curl http://localhost:5000/extractions
    #curl http://localhost:5000/extractions?"url=http://www.bbc.com"
    def get(self): # returns all extractions, or returns a specific extraction based on URL
        args = parser.parse_args()
        url = args['url']
         
        sys.stdout.flush()
        if (url == None) or (url == ''): # requested all extractions
            return extractorLib.Extraction.getAll(), 200 # success
        else: # requested extractions filtered by one url
            ext = extractorLib.Extraction.getExtractionFromURL(url)
            if (ext == None) or (ext == {}):
                return 404 # resource not found
            else:
                return ext, 200 # success

    # curl http://localhost:5000/extractions -d "url=http://www.bbc.com" -X POST -v
    def post(self): # creates a new extraction
        args = parser.parse_args()
        print args
        sys.stdout.flush()
        url = args['url']
        if (url == None) or (url == ''):
            return 400 # bad request
        else:
            ext = extractorLib.Extraction.addExtraction(url)
            if (ext == None) or (ext == {}):
                return 401 # unauthorized request
            else:
                return ext, 200 # success
##
## Actually setup the Api resource routing here
##
api.add_resource(ExtractionList, '/extractions')
api.add_resource(Extraction, '/extractions/<string:extID>')
        
        
        