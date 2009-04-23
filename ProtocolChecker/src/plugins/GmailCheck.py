'''
Created on Apr 15, 2009

@author: scott
'''

import Plugin
import feedparser
import GmailCheckUI

class GmailCheck( Plugin.Plugin ):

    def check( self ):
        uid = self.ui.get_username( )
        password = self.ui.get_password( )
        
        inbox = feedparser.parse( "https://%s:%s@gmail.google.com/gmail/feed/atom%s" % ( uid, password, "" ) )
        
        return self.trigger_alert( len( inbox["entries"] ) > 0 )
    
    def trigger_alert(self, status):
        print status
        return status
    
    def show( self ):
        self.ui.show( )
        return
    
    def __init__( self ):
        self.ui = GmailCheckUI.GmailCheckUI( )
        return