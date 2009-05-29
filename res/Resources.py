'''
Created on Apr 15, 2009

@author: scott
'''

import os, sys

UI_DIR_NAME = "ui"
PLUGIN_DIR_NAME = "plugins"
LAUNCH_DIR = os.path.abspath( sys.path[0] )
DATA_DIRS = [ LAUNCH_DIR ]

def get_ui_asset( asset_name ):
  for base in DATA_DIRS:
      
    asset_path = os.path.join( base, UI_DIR_NAME, asset_name )
    
    if os.path.exists( asset_path ):
      return asset_path
  
def get_plugin_asset( asset_name ):
  for base in DATA_DIRS:
      
    asset_path = os.path.join( base, PLUGIN_DIR_NAME, asset_name )
    
    if os.path.exists( asset_path ):
      return asset_path