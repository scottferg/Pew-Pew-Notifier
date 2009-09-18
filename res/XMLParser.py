# Copyright (c) 2009, William Best and Scott Ferguson
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the software nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY WILLIAM BEST AND SCOTT FERGUSON ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL WILLIAM BEST AND SCOTT FERGUSON BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
