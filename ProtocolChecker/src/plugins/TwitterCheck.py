'''
Created on Apr 15, 2009

@author: scott
'''

import twitter

def twitterFeed(uid,password):
    api = twitter.Api(username=uid,password=password)
    friend_timeline = api.GetFriendsTimeline(uid)
    
    return friend_timeline

#for status in friends:
#    print status.text