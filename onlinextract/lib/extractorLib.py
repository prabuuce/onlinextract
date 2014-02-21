'''
Created on Feb 18, 2014

@author: svattam
'''
from onlinextract.app import flaskApp

from boilerpipe.extract import Extractor, jpype
import requests, justext
from flaskext.mongoalchemy import MongoAlchemy

flaskApp.config['MONGOALCHEMY_DATABASE'] = 'extractions'
db = MongoAlchemy(flaskApp)

class Extraction(db.Document):
    url = db.StringField()
    bpExtract = db.StringField()
    jtExtract = db.StringField()
    
    @staticmethod
    def getExtraction(extID):
        ext = Extraction.query.get(extID)
        if(ext == None):
            return{}
        else:
            return jsonify(ext)
    
    @staticmethod
    def getExtractionFromURL(url):
        ext = Extraction.query.filter(Extraction.url == url).first()
        if(ext == None):
            return{}
        else:
            return jsonify(ext)
    
    @staticmethod
    def addExtraction(url):
        bpExtract = BoilerpipeWrapperWrapper(url).getText()
        jtExtract = JusTextWrapper(url).getText()
        ext = Extraction(url=url, bpExtract=bpExtract, jtExtract=jtExtract)
        ext.save()
        return jsonify(ext)
        
    @staticmethod
    def updateExtraction(extID, url):
        ext = Extraction.query.get(extID)
        ext.url = url
        ext.bpExtract = BoilerpipeWrapperWrapper(ext.url).getText()
        ext.jtExtract = JusTextWrapper(ext.url).getText()
        ext.save()
        return jsonify(ext)
        
    @staticmethod
    def deleteExtraction(extID):
        ext = Extraction.query.get(extID)
        if ext == None:
            return{}
        else:
            ext.remove()
            return jsonify(ext)
        
    @staticmethod
    def getAll():
        ret = {}
        for ext in Extraction.query.all():
            ret.update(jsonify(ext))
        return ret

############## The rest are all helper functions and helper calsses ####################    
def jsonify(Extraction):
    return {str(Extraction.mongo_id):{'url':Extraction.url, 'bpExtract':Extraction.bpExtract, 'jtExtract':Extraction.jtExtract}}

class BoilerpipeWrapperWrapper():
    iUrl = ""
    def __init__(self, url):
        if not jpype.isThreadAttachedToJVM():
            jpype.attachThreadToJVM()
        BoilerpipeWrapperWrapper.iUrl = url
    
    def getText(self):
        try:
            extractor = Extractor(extractor='ArticleExtractor', url=BoilerpipeWrapperWrapper.iUrl)
            return extractor.getText()
        except:
            return ""

class JusTextWrapper():
    iUrl = ""
    def __init__(self, url):
        JusTextWrapper.iUrl = url
        
    def getText(self):
        text = ''
        try:
            response = requests.get(JusTextWrapper.iUrl)
            paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
            for paragraph in paragraphs:
                if not paragraph.is_boilerplate:
                    text += " "+paragraph.text
            return text
        except:
            return ""
