'''
Created on Apr 15, 2009

@author: scott
'''

import Plugin
import feedparser

class GmailCheck(Plugin.Plugin):

    def messageCount(self,uid,password,filter):
        inbox = feedparser.parse("https://%s:%s@gmail.google.com/gmail/feed/atom%s" % (uid, password, filter))
        return self.trigger_alert(len(inbox["entries"]) > 0)