'''
Created on May 31, 2009

@author: Scott Ferguson
'''

import Plugin
import urllib
import json

class LastFM( Plugin.Plugin ):
    API_KEY = '6bd4fd1a3a707c7634941a2920d65dcf'
    SECRET_KEY = 'a20918ddb42bbec4fe005e7f52e501be'

    def check( self ):
        user_list = self.make_request( { 'method':'user.getFriends', 'user':'scottferg' } )

        for user in json.loads( user_list )['friends']['user']:
            print user['name']
            response = self.make_request( { 'method':'user.getrecenttracks', 'user':user['name'] } )

            for result in json.loads( response )['recenttracks']['track']:
                if 'nowplaying' in result:
                    return self.trigger_alert( { 'alert':True, 'title':user['name'], 'message':result['artist']['#text'] + " - " + result['name'] } )

        return self.trigger_alert( False )

    def make_request( self, params ):
        param_string = "&".join( [ "%s=%s" % ( param, value ) for param, value in params.items( ) ] )

        return urllib.urlopen( "http://ws.audioscrobbler.com/2.0/?%s&format=json&api_key=%s" % ( param_string, self.API_KEY ) ).read( )

    def __init( self ):
        self.make_request( )
        Plugin.Plugin.__init__(self)
