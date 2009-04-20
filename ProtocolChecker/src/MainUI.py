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
ACTIVE_LIST = []

def set_import_string(class_name):
    IMPORT_STRING.append(class_name)
    
def call_import_string():
    for import_func in IMPORT_STRING:
        exec import_func

class MainUI:
    
    def on_cmdCheck_clicked(self,widget,data=None):
        self.check()
    
    def on_cmdConfigure_clicked(self,widget,data=None):
        plugin_obj = PLUGIN_LIST[ self.current_config - 1 ]
        plugin_obj.show()
            
    def on_plugin_select(self,widget,data=None):
        (model, iter) = widget.get_selected()
        self.current_config = model.get_value(iter, 0)
        
    def check(self):
        for plugin_obj in PLUGIN_LIST:
            print plugin_obj.check()
            
    def make_model(self, list):
        self.tree_store = gtk.TreeStore( int, str, 'gboolean' )
                
        for item in list:
            print item[0]
            print item[1]
            parent = self.tree_store.append( None, [item[0], item[1], None] )
        return
    
    def get_model(self):
        if self.tree_store:
            return self.tree_store 
        else:
            return None
            
    def make_view( self, model ):
        """ Form a view for the Tree Model """
        self.view = gtk.TreeView( model )
        
        self.id_renderer = gtk.CellRendererText()
        self.title_renderer = gtk.CellRendererText()
        
        self.active_renderer = gtk.CellRendererToggle()
        self.active_renderer.set_property('activatable', True)
        self.active_renderer.connect( 'toggled', self.col_toggled_cb, model )
        
        self.column0 = gtk.TreeViewColumn("ID", self.id_renderer, text=0)
        self.column0.set_visible( False )
        self.column1 = gtk.TreeViewColumn("Name", self.title_renderer, text=1)
        self.column2 = gtk.TreeViewColumn("Complete", self.active_renderer )
        self.column2.add_attribute( self.active_renderer, "active", 2)
        
        self.view.append_column( self.column0 )
        self.view.append_column( self.column1 )
        self.view.append_column( self.column2 )
        self.view.set_expander_column( self.column2 )
        
        return self.view
    
    def col_toggled_cb( self, cell, path, model ):
        model[path][2] = not model[path][2]
        return        
    
        # Is this a memory leak?  Probably.  Whoops.
        self.timeoutId  = gobject.timeout_add(15000,self.check)
    
    def import_plugins(self):
        
        list = self.plugin_db.fetch_available_plugins()

        for row in list:
            
            class_import_string = "from plugins import " + row[3]
            set_import_string(class_import_string)
            call_import_string()
            exec class_import_string
            
            exec "item = " + row[3] + "." + row[3] + "()"
            PLUGIN_LIST.append(item)
            
    def activate(self,widget,data=None):
            self.connect_ui()
            
    def delete_event(self,widget,event,data=None):
        return False
    
    def destroy(self,widget,data=None):
        gtk.main_quit()
        
    def connect_ui(self):

        glade = gtk.glade.XML(Resources.get_ui_asset("MainUI.glade"))
        
        self.statusicon = gtk.StatusIcon()
        self.statusicon.set_from_stock(gtk.STOCK_ABOUT)
        self.statusicon.connect("activate", self.activate)
        self.statusicon.set_visible(True) 
        
        self.cmdConfigure = glade.get_widget("cmdConfigure")
        self.cmdCheck = glade.get_widget("cmdCheck")
        self.listVbox = glade.get_widget("listVbox")
        self.window = glade.get_widget("mainWindow")
        
        self.store = self.make_model(self.plugin_db.fetch_available_plugins())    
        
        self.mdl = self.get_model()
        self.view = self.make_view(self.mdl)
        
        self.tree_select = self.view.get_selection()
        self.tree_select.set_mode(gtk.SELECTION_SINGLE)
        self.tree_select.connect("changed", self.on_plugin_select)
                
        self.listVbox.pack_start(self.view)
        
        self.window.connect("destroy", self.destroy)
        
        glade.signal_autoconnect(self)
        
        self.window.show_all()
    
    def __init__(self):        
        
        self.current_config = 1
        self.plugin_db = PluginDatabase.PluginDatabase()
        
        self.connect_ui()
        
        self.import_plugins()
        
        self.timeoutId  = gobject.timeout_add(15000,self.check)
                
    def main(self):
        gtk.main()
        
if __name__ == "__main__":
    protocol = MainUI()
    protocol.main()