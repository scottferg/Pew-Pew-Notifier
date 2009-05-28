'''
Created on Apr 19, 2009

@author: scott
'''

from pysqlite2 import dbapi2 as sqlite
import glob
import XMLParser

class PluginDatabase:
    
    def fetch_available_plugins( self ):
        self.cursor.execute( 'SELECT * FROM plugins' )
        
        return self.cursor
        
    def fetch_plugin( self, pluginId ):
        self.cursor.execute( 'SELECT * FROM plugins WHERE id=?', ( pluginId ) )
        
        return self.cursor
    
    def write_available_plugins( self ):
        
        xml_fileset = glob.glob( 'plugins/*.xml' )
        
        for xml_file in xml_fileset:
            data = XMLParser.parseFile( xml_file )
            self.cursor.execute( 'INSERT INTO plugins VALUES (null, ?, ?, ?)', ( data['plugin']['name'], data['description'], data['main_module'] ) )
            
        self.connect.commit( )
    
    def create_plugin_table( self ):
        self.cursor.execute( 'CREATE TABLE plugins (id INTEGER PRIMARY KEY, name VARCHAR(50), description VARCHAR(140), module VARCHAR(50))' )
    
    def __init__( self ):
        
        self.connect = sqlite.connect( ':memory:' )
        self.cursor = self.connect.cursor( )
        
        self.create_plugin_table( )
        self.write_available_plugins( )
        self.fetch_available_plugins( )