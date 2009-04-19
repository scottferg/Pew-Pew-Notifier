'''
Created on Apr 19, 2009

@author: scott
'''
from xml.sax import saxutils
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return ' '.join(text.split())

class ParsePlugin(saxutils.DefaultHandler):
    
    def __init__(self):
        # Initialize the flag to false
        self.plugin_info = []
        self.inPluginContent = 0
    
    def startElement(self, root, attrs):
        if root == 'plugin':
            name = attrs.get('name', None)
            self.plugin_info.append(normalize_whitespace(name))
        
        elif root == 'description':
            self.inPluginContent = 1
            self.plugin_description = ""
            
    def characters(self, ch):
        if self.inPluginContent:
            self.plugin_description = self.plugin_description + ch
            
    def endElement(self, name):
        if name =='description':
            self.inPluginContent = 0
            self.plugin_info.append(normalize_whitespace(self.plugin_description))
    
    def fetchDataSet(self):
        return self.plugin_info
        
class XMLParser:
    
    def return_result(self):
        return self.default_handler.fetchDataSet()
    
    def __init__(self,file):
        self.parser = make_parser()
        self.parser.setFeature(feature_namespaces, 0)
        self.default_handler = ParsePlugin()
        self.parser.setContentHandler(self.default_handler)
        self.parser.parse(file)
