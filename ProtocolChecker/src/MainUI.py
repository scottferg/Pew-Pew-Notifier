'''
Created on Apr 15, 2009

@author: scott
'''

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

import GmailCheck
import Resources

class ProtocolCheckUI:
    
    def on_cmdLogin_clicked(self,widget,data=None):
        print GmailCheck.messageCount(self.txtUsername.get_text(),self.txtPassword.get_text(),"")
        return True
    
    def on_cmdQuit_clicked(self,widget,data=None):
        gtk.main_quit()
    
    def delete_event(self,widget,event,data=None):
        return False
    
    def destroy(self,widget,data=None):
        gtk.main_quit()
    
    def __init__(self):
        
        print Resources.get_ui_asset("GmailCheckUI.glade")
        
#        glade = gtk.glade.XML(Resources.get_ui_asset("GmailCheckUI.glade"))
        glade = gtk.glade.XML("GmailCheckUI.glade")
        self.txtUsername = glade.get_widget("txtUsername")
        self.txtPassword = glade.get_widget("txtPassword")
        self.window = glade.get_widget("mainWindow")
        
        glade.signal_autoconnect(self)
        
        self.window.show()
        
    def main(self):
        gtk.main()
        
if __name__ == "__main__":
    protocol = ProtocolCheckUI()
    protocol.main()