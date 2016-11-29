#!/usr/bin/python
################################################################################
# CREDENTIALS
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/28/2016 Original construction
################################################################################

import cherrypy

from base64 import b64decode

class Credentials(object):
    @cherrypy.expose
    def set_ssh_password(self, b64str):
        cherrypy.session['ssh password'] = b64decode(b64str)
    
    @cherrypy.expose
    def set_mysql_password(self, b64str):
        cherrypy.session['mysql password'] = b64decode(b64str)
    
    @cherrypy.expose
    def set_ssh_username(self, username):
        cherrypy.session['ssh username'] = username
    
    @cherrypy.expose
    def set_mysql_username(self, username):
        cherrypy.session['mysql username'] = username
