'''
Created on Apr 15, 2009

@author: scott
'''

import Plugin
import GmailCheckUI
import urllib2
import base64
from res import XMLParser

class GmailCheck( Plugin.Plugin ):

    def check( self ):

        request = urllib2.Request( "https://gmail.google.com/gmail/feed/atom" )

        base64string = base64.encodestring( '%s:%s' % ( self.ui.get_username( ), self.ui.get_password( ) ) )[:-1]
        request.add_header( "Authorization", "Basic %s" % base64string )

        response = urllib2.urlopen( request )

        data_set = XMLParser.parseStream( response.read( ) )

        response.close( )

        return self.trigger_alert( int( data_set['fullcount'] ) > 0, data_set['name'], data_set['title'] )
    
    def trigger_alert(self, status, sender, subject ):
        result = {}

        result['alert'] = status
        result['title'] = sender
        result['message'] = subject

        print status
        return result
    
    def show( self ):
        self.ui.show( )
        return
    
    def __init__( self ):
        self.ui = GmailCheckUI.GmailCheckUI( )
        return
