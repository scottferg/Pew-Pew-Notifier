'''
Created on Apr 19, 2009

@author: scott
'''

class Plugin:
    
    def trigger_alert( self, status ):
        print "Status: %s" % status
        return status
    
    def show( self ):
        return True
    
    def check( self ):
        return True
