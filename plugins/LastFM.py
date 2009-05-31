'''
Created on May 31, 2009

@author: Scott Ferguson
'''

import Plugin
import urllib

from res import XMLParser

class LastFM( Plugin.Plugin ):
    API_KEY = '6bd4fd1a3a707c7634941a2920d65dcf'
    SECRET_KEY = 'a20918ddb42bbec4fe005e7f52e501be'

    def check( self ):
        self.make_request( { 'method':'user.getrecenttracks', 'user':'scottferg' } )

    def make_request( self, params ):
        param_string = "&".join( [ "%s=%s" % ( param, value ) for param, value in params.items( ) ] )

        response = urllib.urlopen( "http://ws.audioscrobbler.com/2.0/?%s&api_key=%s" % ( param_string, self.API_KEY ) ).read( )
        return XMLParser.parseStream( response )

    def __init( self ):
        self.make_request( )
