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
            self.description = ""
        elif name == 'main_module':
            self.inMainModule = True
            self.main_module = ""

    def endElement( self, name ):
        if name == 'description':
            self.inDescription = False
            self.description = self.normalizeWhitespace( self.description )
        elif name == 'main':
            self.inMainModule = False
            self.main_module = self.normalizeWhitespace( self.main_module )

    def characters( self, data ):
        if self.inDescription:
            self.description = self.description + data 
        elif self.inMainModule:
            # Why does this reference to data need the whitespace removed and not
            # the description field?
            self.main_module = self.main_module + self.normalizeWhitespace( data )

    def normalizeWhitespace( self, text ):
        """Remove redundant whitespace from a string"""
        return " ".join( text.split( ) )

    def fetchSet( self ):

        print self.name
        print "Description: " + self.description
        print "Main Module: " + self.main_module

        return { 'name' : self.name, 'description' : self.description, 'main_module' : self.main_module }

    def __init__( self, file ):
        self.inDescription = False
        self.inMainModule = False

        parser = expat.ParserCreate( )
        parser.StartElementHandler = self.startElement
        parser.EndElementHandler = self.endElement
        parser.CharacterDataHandler = self.characters
        parser.ParseFile( open( file, "r" ) )
