'''
Created on Apr 17, 2009

@author: scott
'''

'''
Created on Apr 15, 2009

@author: scott
'''

import pygtk
pygtk.require( "2.0" )
import gtk
import gtk.glade

import Resources

class TwitterCheckUI:
    
    def get_username( self ):
        return self.username
    
    def get_password( self ):
        return self.password
    
    def get_update(self):
        if self.update == "1 Minute":
            return 60000
        elif self.update == "5 Minutes":
            return 60000 * 5
        elif self.update == "10 Minutes":
            return 60000 * 10
        elif self.update == "15 Minutes":
            return 60000 * 15
        elif self.update == "20 Minutes":
            return 60000 * 20
        elif self.update == "30 Minutes":
            return 60000 * 30

    def on_cmdLogin_clicked( self, widget, data = None ):
        self.username = self.txtUsername.get_text( )
        self.password = self.txtPassword.get_text( )
        self.update = self.txtUpdate.get_active_text( )
        self.window.hide( )
            
    def delete_event( self, widget, event, data = None ):
        return False
    
    def destroy( self, widget, data = None ):
        self.window.hide( )
    
    def connect_ui( self ):

        self.username = ''
        self.password = ''
        self.update = '5 Minutes'

        glade = gtk.glade.XML( Resources.get_plugin_asset( "./TwitterCheckUI.glade" ) )
        self.txtUsername = glade.get_widget( "txtUsername" )
        self.txtPassword = glade.get_widget( "txtPassword" )
        self.txtUpdate = glade.get_widget("txtTimeLimit")
        
        self.txtUsername.set_text( self.username )
        self.txtPassword.set_text( self.password )
        self.txtUpdate.set_active( 1 )
        
        self.window = glade.get_widget( "mainWindow" )
                
        glade.signal_autoconnect( self )
        
    def show( self ):
        
        self.window.show( )
            
    def __init__( self ):        
        
        self.connect_ui( )
