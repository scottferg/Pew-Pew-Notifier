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

import twitter
import Plugin
import TwitterCheckUI

class TwitterCheck( Plugin.Plugin ):
    def check(self):
        self.counter += 15000
        
        if self.counter >= self.ui.get_update():
            self.counter = 0
            return self.update()
        return ""

    def trigger_alert(self, status):
        print status
        return status
            
    def update( self ):
        username = self.ui.get_username()
        password = self.ui.get_password()
        api = twitter.Api( username, password )
        friend_timeline = api.GetFriendsTimeline( )
        return self.trigger_alert( len(friend_timeline) )

    def show( self ):
        self.ui.show( )
        return
    
    def __init__( self ):
        self.since = 0
        self.ui = TwitterCheckUI.TwitterCheckUI( )
        self.counter = 0
        Plugin.Plugin.__init__(self)
        return
