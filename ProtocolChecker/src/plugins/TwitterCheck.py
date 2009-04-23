'''
Created on Apr 15, 2009

@author: scott
'''

import twitter
import Plugin
import TwitterCheckUI

class TwitterCheck( Plugin.Plugin ):
    def check(self):
        if self.counter == self.ui.get_update():
            self.counter = 0
            self.update()
        else:
            self.counter += 15000
    def update( self ):
        
        api = twitter.Api( username = ui.get_username, password = ui.get_password )
        friend_timeline = api.GetFriendsTimeline( username, None, None, None, None )
    
        return trigger_alert( friend_timeline )

    def show( self ):
        self.ui.show( )
        return
    
    def __init__( self ):
        self.ui = TwitterCheckUI.TwitterCheckUI( )
        self.counter = 0
        return
