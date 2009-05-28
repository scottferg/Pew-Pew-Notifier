'''Created on Apr 19, 2009
 
@author: scott
'''
from xml.parsers import expat

class Parser( ):
    def parse( self ):
        return self.data_set
    
    def startElement( self, name, attrs ):
        self.current_element = name

        print self.data_set 

        if len( attrs ) > 0:
            self.data_set[ name ] = dict( [ ( key, value ) for key, value in attrs.iteritems( ) ] )

    def endElement( self, name ):
        self.current_element = ""
         
    def characters( self, data ):
        self.data_set[ self.current_element ] = self.normalizeWhitespace( data )

    def normalizeWhitespace( self, text ):
        """Remove redundant whitespace from a string"""
        return " ".join( text.split( ) )
 
    def __init__( self, file ):
        self.data_set = {}
        self.current_element = ""

        parser = expat.ParserCreate( )
        parser.StartElementHandler = self.startElement
        parser.EndElementHandler = self.endElement
        parser.CharacterDataHandler = self.characters
        parser.ParseFile( open( file, "r" ) )

        print self.data_set
