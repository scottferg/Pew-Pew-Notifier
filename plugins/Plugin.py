'''
Created on Apr 19, 2009

@author: scott
'''

import observer

class Plugin(observer.Subject):
    
    def __init__(self):
        observer.Subject.__init__(self)

    def trigger_alert( self, status ):
        print "Status: %s" % status
        return status
    
    def show( self ):
        return True
    
    def check( self ):
        return True
