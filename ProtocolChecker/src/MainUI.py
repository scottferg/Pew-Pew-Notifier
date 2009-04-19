'''
Created on Apr 19, 2009

@author: scott
'''

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import gobject

import threading

import Resources
import PluginDatabase

IMPORT_STRING = []
PLUGIN_LIST = []

def set_import_string(class_name):
    IMPORT_STRING.append(class_name)

class MainUI:
    
    def on_cmdCheck_clicked(self,widget,data=None):
        self.check()
    
    def on_cmdConfigure_clicked(self,widget,data=None):
        for import_func in IMPORT_STRING:
            exec import_func
        
        for plugin_obj in PLUGIN_LIST:
            plugin_obj.show()
        
    def check(self):
        for import_func in IMPORT_STRING:
            exec import_func
        
        for plugin_obj in PLUGIN_LIST:
            print plugin_obj.check()
            
        # Is this a memory leak?  Probably.  Whoops.
        self.timeoutId  = gobject.timeout_add(15000,self.check)
    
    def import_plugins(self):
        
        list = self.plugin_db.fetch_available_plugins()
        
        for row in list:
            
            class_import_string = "from plugins import " + row[3]
            set_import_string(class_import_string)
            exec class_import_string
            
            exec "item = " + row[3] + "." + row[3] + "()"
            PLUGIN_LIST.append(item)
            
            self.lblTitle.set_text(row[1])
            self.lblDescription.set_text(row[2])
            
        print PLUGIN_LIST
            # only imports within the scope of import_plugins()
    
    def activate(self,widget,data=None):
            self.connect_ui()
            
    def delete_event(self,widget,event,data=None):
        return False
    
    def destroy(self,widget,data=None):
        gtk.main_quit()
        
    def connect_ui(self):

        glade = gtk.glade.XML(Resources.get_ui_asset("MainUI.glade"))
        self.cmdConfigure = glade.get_widget("cmdConfigure")
        self.cmdCheck = glade.get_widget("cmdCheck")
        self.lblTitle = glade.get_widget("lblTitle")
        self.lblDescription = glade.get_widget("lblDescription")
        self.window = glade.get_widget("mainWindow")
        
        self.window.connect("destroy", self.destroy)
        
        glade.signal_autoconnect(self)
        
        self.window.show()
    
    def __init__(self):        
#        glade = gtk.glade.XML(Resources.get_ui_asset("GmailCheckUI.glade"))
        self.statusicon = gtk.StatusIcon()
        self.statusicon.set_from_stock(gtk.STOCK_ABOUT)
        self.statusicon.connect("activate", self.activate)
#        self.staticon.connect("popup_menu", self.popup)
        self.statusicon.set_visible(True) 
        
        self.connect_ui()
        
        self.plugin_db = PluginDatabase.PluginDatabase()
        self.import_plugins()
        
        self.timeoutId  = gobject.timeout_add(15000,self.check)
        
#        self.main_timer = threading.Timer(5.0, self.check)
#        self.main_timer.start() # after 30 seconds, "hello, world" will be printed
        
    def main(self):
        gtk.main()
        
if __name__ == "__main__":
    protocol = MainUI()
    protocol.main()