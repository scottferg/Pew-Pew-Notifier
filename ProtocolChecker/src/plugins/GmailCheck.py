'''
Created on Apr 15, 2009

@author: scott
'''

import feedparser

def messageCount(uid,password,filter):
    inbox = feedparser.parse("https://%s:%s@gmail.google.com/gmail/feed/atom%s" % (uid, password, filter))
    return len(inbox["entries"])