#!/usr/bin/python
################################################################################
# CREDENTIALS
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/28/2016 Original construction
# 02/22/2017 Updated methods to put data into user objects
################################################################################

import cherrypy
import traceback

from base64 import b64decode
from .messaging import add_message
from ..model.document import Collection

class Credentials(object):
    @cherrypy.expose
    def set_ssh_password(self, b64str):
        add_message("credentials controller: set SSH password...")
        try:
            users = Collection("users")
            for user in users.find(sessionid = cherrypy.session.id):
                user.object['ssh password'] = b64decode(b64str)
                user.set()
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def set_mysql_password(self, b64str):
        add_message("credentials controller: set MySQL password...")
        try:
            users = Collection("users")
            for user in users.find(sessionid = cherrypy.session.id):
                user.object['mysql password'] = b64decode(b64str)
                user.set()

        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def set_ssh_username(self, username):
        add_message("credentials controller: set SSH username: {0}".format(username))
        users = Collection("users")
        for user in users.find(sessionid = cherrypy.session.id):
            user.object['ssh username'] = username
            user.set()
    
    @cherrypy.expose
    def set_mysql_username(self, username):
        add_message("credentials controller: set MySQL username: {0}".format(username))
        users = Collection("users")
        for user in users.find(sessionid = cherrypy.session.id):
            user.object['mysql username'] = username
            user.set()