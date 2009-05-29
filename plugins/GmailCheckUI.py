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

from res import Resources

class GmailCheckUI:
    
    def get_username( self ):
        return self.username
    
    def get_password( self ):
        return self.password
    
    def on_cmdLogin_clicked( self, widget, data = None ):
        self.username = self.txtUsername.get_text( )
        self.password = self.txtPassword.get_text( )
        self.window.hide( )
            
    def delete_event( self, widget, event, data = None ):
        return False
    
    def destroy( self, widget, data = None ):
        self.window.hide( )
    
    def connect_ui( self ):

        self.username = ''
        self.password = ''

        glade = gtk.glade.XML( Resources.get_plugin_asset( "./GmailCheckUI.glade" ) )
        self.txtUsername = glade.get_widget( "txtUsername" )
        self.txtPassword = glade.get_widget( "txtPassword" )
        
        self.txtUsername.set_text( self.username )
        self.txtPassword.set_text( self.password )
        
        self.window = glade.get_widget( "mainWindow" )
                
        glade.signal_autoconnect( self )
        
    def show( self ):
        
        self.window.show( )
            
    def __init__( self ):        
        
        self.connect_ui( )
