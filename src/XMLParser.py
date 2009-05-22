'''
Created on Apr 19, 2009

@author: scott
'''
from xml.parsers import expat

class Parser( ):
    
    def startElement( self, name, attrs ):
        if name == 'plugin':
            self.name = attrs['name']
        elif name == 'description':
            self.inDescription = True
        elif name == 'main_module':
            self.inMainModule = True

    def endElement( self, name ):
        if name == 'description':
            self.inDescription = False
        elif name == 'main':
            self.inMainModule = False

    def characters( self, data ):
        print "Description: " + self.normalizeWhitespace( data )

        if self.inDescription:
            self.description = self.normalizeWhitespace( data )
            self.inDescription = False
        elif self.inMainModule:
            self.main_module = self.normalizeWhitespace( data )
            self.inMainModule = False

    def normalizeWhitespace( self, text ):
        """Remove redundant whitespace from a string"""
        return " ".join( text.split( ) )

    def fetchSet( self ):

        print self.name

        return { 'name' : self.name, 'description' : self.description, 'main_module' : self.main_module }

    def __init__( self, file ):
        self.inDescription = False
        self.inMainModule = False

        parser = expat.ParserCreate( )
        parser.StartElementHandler = self.startElement
        parser.EndElementHandler = self.endElement
        parser.CharacterDataHandler = self.characters
        parser.ParseFile( open( file, "r" ) )
