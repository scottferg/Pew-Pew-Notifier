'''
Created on Apr 19, 2009

@author: scott
'''

class Plugin:
    
    def trigger_alert(self, status):
        return status
    
    def show(self):
        return True
    
    def check(self):
        return True
