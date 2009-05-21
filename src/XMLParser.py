'''
Created on Apr 19, 2009

@author: scott
'''
from xml.sax import saxutils
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces

def normalize_whitespace( text ):
    "Remove redundant whitespace from a string"
    return ' '.join( text.split( ) )

class ParsePlugin( saxutils.DefaultHandler ):
    
    def __init__( self ):
        # Initialize the flag to false
        self.plugin_info = [ ]
        self.inDescription = 0
        self.inMainModule = 0
    
    def startElement( self, root, attrs ):
        if root == 'plugin':
            name = attrs.get( 'name', None )
            self.plugin_info.append( normalize_whitespace( name ) )
        
        elif root == 'description':
            self.inDescription = 1
            self.plugin_description = ""
            
        elif root == 'main_module':
            self.inMainModule = 1
            self.plugin_module = ""
            
    def characters( self, ch ):
        if self.inDescription:
            self.plugin_description = self.plugin_description + ch
        elif self.inMainModule:
            self.plugin_module = self.plugin_module + ch
            
    def endElement( self, name ):
        if name =='description':
            self.inDescription = 0
            self.plugin_info.append( normalize_whitespace( self.plugin_description ) )
        elif name =='main_module':
            self.inMainModule = 0
            self.plugin_info.append( normalize_whitespace( self.plugin_module ) )
    
    def fetchDataSet( self ):
        return self.plugin_info
        
class XMLParser:
    
    def return_result( self ):
        return self.default_handler.fetchDataSet( )
    
    def __init__( self, file ):
        self.parser = make_parser( )
        self.parser.setFeature( feature_namespaces, 0 )
        self.default_handler = ParsePlugin( )
        self.parser.setContentHandler( self.default_handler )
        self.parser.parse( file )
