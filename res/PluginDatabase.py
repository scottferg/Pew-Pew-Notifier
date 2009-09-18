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
