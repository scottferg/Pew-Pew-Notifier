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
pygtk.require("2.0")
import gtk
import gtk.glade
import gobject

import threading
import time

import observer

import external

from res import Resources
from res import PluginDatabase

gobject.threads_init()

class PluginThread(threading.Thread):
    def __init__(self, plugin, terminate = False):
        self.plugin = plugin
        self.terminate = terminate
        threading.Thread.__init__(self)

    def run(self):
        # Check for updates every 15 seconds
        while True:
            self.check()

            if self.terminate:
                print 'Thread terminated'
                break

            time.sleep(15)

    def check(self):
        check = (getattr(self.plugin, 'check'))

        if callable(check) is True:
            result = check()
            
            if type(result) is type({}) and result['alert']:
                # Notify any observers that we've received an
                # alert
				self.plugin.notify(True)

class PluginHandler(observer.Observer):
    # Do we need a constructor here?
    def __init__(self):
        pass

    def update(self, *args):
        if args[1] is True:
            # Handle your notifications here
            external.notify()

class MainUI:
    
    def on_cmdCheck_clicked(self, widget, data = None):
        self.check()

    def check(self, data=None):
        for index,plugin_obj in self.plugin_list.iteritems():
            plugin_obj.attach(PluginHandler())
            # Tell the thread to terminate after it completes a single pass
            PluginThread(plugin_obj, True).start()
    
    def on_cmdConfigure_clicked(self, widget, data = None):
        plugin_obj = self.plugin_list[self.current_config]
        plugin_obj.show()
         
    def on_plugin_select(self, widget, data = None):
        (model, iter) = widget.get_selected()
        self.current_config = model.get_value(iter, 0)
        
    def make_model(self, list):
        self.tree_store = gtk.TreeStore(int, str, 'gboolean')

        for item in list:
            parent = self.tree_store.append(None, [item[0], item[1], None])

    def get_model(self):
        if self.tree_store:
            return self.tree_store 
        else:
            return None
            
    def make_view(self, model):
        """ Form a view for the Tree Model """
        self.view = gtk.TreeView(model)
        
        self.id_renderer = gtk.CellRendererText()
        self.title_renderer = gtk.CellRendererText()
        
        self.active_renderer = gtk.CellRendererToggle()
        self.active_renderer.set_property('activatable', True)
        self.active_renderer.connect('toggled', self.on_column_toggled, model)

        self.column0 = gtk.TreeViewColumn("ID", self.id_renderer, text = 0)
        self.column0.set_visible(False)

        self.column1 = gtk.TreeViewColumn("Name", self.title_renderer, text = 1)
        self.column1.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.column1.set_expand(True)

        self.column2 = gtk.TreeViewColumn("Enabled", self.active_renderer)
        self.column2.add_attribute(self.active_renderer, "active", 2)
        self.column2.set_alignment(0.5)
        self.column2.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        self.column2.set_expand(False)

        self.view.append_column(self.column0)
        self.view.append_column(self.column1)
        self.view.append_column(self.column2)
        self.view.set_expander_column(self.column2)
        
        return self.view
    
    def on_column_toggled(self, cell, path, model):
        model[path][2] = not model[path][2]
        
        if model[path][2]:
            list = self.plugin_db.fetch_plugin(str(model[path][0]))

            for row in list:
                # Load and instantiate the new plugin
                exec "from plugins import " + row[3]
                exec "item = " + row[3] + "." + row[3] + "()"
                # Attach an observer to the plugin
                item.attach(PluginHandler())
                # Add the plugin instance to the plugin list
                self.plugin_list[row[0]] = item
                # Fire off the plugin in it's own thread
                PluginThread(item).start()
        else:
            # Otherwise, we are turning it off, so remove it
            # from the active plugin list
            del self.plugin_list[model[path][0]]
        
        return        
            
    def activate(self, widget, data = None):
            self.connect_ui()
            
    def toggle_window(self, widget, data = None):
        if self.window.get_property("visible"):
            self.window.hide()
        else:
            self.window.show()        
            
    def popup_menu_cb(self, widget, button, time, data = None): 
        if button == 3: 
            if data: 
                data.show_all() 
                data.popup(None, None, None, 3, time) 
            
    def delete_event(self, widget, event, data = None):
        self.toggle_window(self.window)

        return True
    
    def destroy(self, widget, data = None):
        gtk.main_quit()
        
    def connect_ui(self):

        glade = gtk.glade.XML(Resources.get_ui_asset("MainUI.glade"))
        
        menu = gtk.Menu() 
        menuItem = gtk.ImageMenuItem(gtk.STOCK_CONNECT)
        menuItem.connect('activate', self.check)
        menu.append(menuItem)
        menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT) 
        menuItem.connect('activate', self.destroy) 
        menu.append(menuItem) 
        
        self.statusicon = gtk.status_icon_new_from_file("ui/Pew_Checker_Icon.svg")
        self.statusicon.connect("activate", self.toggle_window)
        self.statusicon.connect("popup-menu", self.popup_menu_cb, menu)
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
        
        self.window.connect("delete_event", self.delete_event)
        
        glade.signal_autoconnect(self)
        external.init()
        self.window.show_all()
    
    def __init__(self):
        self.plugin_db = PluginDatabase.PluginDatabase()
        self.plugin_list = {}
        
        self.connect_ui()
                
    def main(self):
        gtk.main()
        
if __name__ == "__main__":
    protocol = MainUI()
    protocol.main()
