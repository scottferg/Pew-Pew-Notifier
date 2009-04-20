'''
Created on Apr 15, 2009

@author: scott
'''

import twitter
import Plugin

class TwitterCheck(Plugin.Plugin):
    def twitterFeed(uid,password):
        api = twitter.Api(username=uid,password=password)
        friend_timeline = api.GetFriendsTimeline(uid)
    
        return friend_timeline

    def show(self):
        return
    
    def __init__(self):
        return

#for status in friends:
#    print status.text