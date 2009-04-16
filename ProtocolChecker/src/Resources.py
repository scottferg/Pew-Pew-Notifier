'''
Created on Apr 15, 2009

@author: scott
'''

import os
import sys

UI_DIR_NAME = "ui"
LAUNCH_DIR = os.path.abspath(sys.path[0])
DATA_DIRS = [LAUNCH_DIR]

def get_ui_asset(asset_name):
        
    for base in DATA_DIRS:
        
        print sys.path[0]
        
#        asset_path = os.path.join(base, UI_DIR_NAME, asset_name)
        asset_path = str.join( "../ui", asset_name )
        if os.path.exists(asset_path):
            return asset_path