'''
Created on Apr 15, 2009

@author: scott
'''

import twitter
import Plugin
import TwitterCheckUI

class TwitterCheck( Plugin.Plugin ):
    def check(self):
        self.counter += 15000
        
        if self.counter >= self.ui.get_update():
            self.counter = 0
            self.update()
            
    def update( self ):
        username = self.ui.get_username()
        password = self.ui.get_password()
        api = twitter.Api( username, password)
        friend_timeline = api.GetFriendsTimeline( )
        print "UPDATE"
        return self.trigger_alert( friend_timeline )

    def show( self ):
        self.ui.show( )
        return
    
    def __init__( self ):
        self.since = 0
        self.ui = TwitterCheckUI.TwitterCheckUI( )
        self.counter = 0
        return
