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

import pygtk
pygtk.require( "2.0" )
import gtk
import gtk.glade

from res import Resources

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
