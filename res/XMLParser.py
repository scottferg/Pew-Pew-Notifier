'''Created on Apr 19, 2009
 
@author: scott
'''
from xml.parsers import expat

data_set = {}
current_element = ""

def startElement( name, attrs ):
    global current_element
    
    current_element = name

    if len( attrs ) > 0:
        data_set[ current_element ] = dict( [ ( key, value ) for key, value in attrs.iteritems( ) ] )

def endElement( name ):
    global current_element
    current_element = ""

def characters( data ):
    global current_element

    if data:
        # Currently this won't read an element with properties and a value
        try:
            if type( data_set[ current_element ] ) is type( {} ): 
                return

            data_set[ current_element ] = normalizeWhitespace( str( data_set[ current_element ] ) + data )
        except KeyError:
            data_set[ current_element ] = data 

def normalizeWhitespace( text ):
    """Remove redundant whitespace from a string"""
    return " ".join( text.split( ) )

def initialize( ):
    global data_set
    global current_element

    data_set = {}
    current_element = ""

    parser = expat.ParserCreate( )
    parser.StartElementHandler = startElement
    parser.EndElementHandler = endElement
    parser.CharacterDataHandler = characters

    return parser

def parseStream( uri ):
    """
    Parse an XML stream and return a dictionary containing the dataset
    """
    initialize( ).Parse( uri, 1 )

    return data_set

def parseFile( file ):
    """
    Parse an XML file and return a dictionary containing the dataset
    """
    initialize( ).ParseFile( open( file, "r" ) )

    return data_set
