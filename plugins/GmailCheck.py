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

import Plugin
import GmailCheckUI

import urllib2
import base64

from urllib2 import HTTPError

from res import XMLParser

class GmailCheck( Plugin.Plugin ):

    def check( self ):

        request = urllib2.Request( "https://gmail.google.com/gmail/feed/atom" )

        base64string = base64.encodestring( '%s:%s' % ( self.ui.get_username( ), self.ui.get_password( ) ) )[:-1]
        request.add_header( "Authorization", "Basic %s" % base64string )

        try:
            response = urllib2.urlopen( request )
        except HTTPError:
            # Don't do anything if there is an HTTP error
            return False

        data_set = XMLParser.parseStream( response.read( ) )

        response.close( )

        return self.trigger_alert( int( data_set['fullcount'] ) > 0, data_set['name'], data_set['title'] )
    
    def trigger_alert(self, status, sender, subject ):
        return { 'alert':status, 'title':sender, 'message':subject } 
    
    def show( self ):
        self.ui.show( )
        return
    
    def __init__( self ):
        self.ui = GmailCheckUI.GmailCheckUI( )
        Plugin.Plugin.__init__(self)
        
        return
