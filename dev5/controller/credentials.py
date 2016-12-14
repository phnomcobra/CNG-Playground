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
import traceback

from base64 import b64decode
from .messaging import add_message

class Credentials(object):
    @cherrypy.expose
    def set_ssh_password(self, b64str):
        add_message("credentials controller: set SSH password...")
        try:
            cherrypy.session['ssh password'] = b64decode(b64str)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def set_mysql_password(self, b64str):
        add_message("credentials controller: set MySQL password...")
        try:
            cherrypy.session['mysql password'] = b64decode(b64str)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def set_ssh_username(self, username):
        add_message("credentials controller: set SSH username: {0}".format(username))
        cherrypy.session['ssh username'] = username
    
    @cherrypy.expose
    def set_mysql_username(self, username):
        add_message("credentials controller: set MySQL username: {0}".format(username))
        cherrypy.session['mysql username'] = username