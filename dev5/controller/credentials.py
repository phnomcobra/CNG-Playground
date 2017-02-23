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
# 02/23/2017 Added MUTEXs to mitigate race condition with user objects
################################################################################

import cherrypy
import traceback

from base64 import b64decode
from threading import Lock
from .messaging import add_message
from ..model.document import Collection

global global_cred_lock
global_cred_lock = Lock()

class Credentials(object):
    @cherrypy.expose
    def set_ssh_password(self, b64str):
        add_message("credentials controller: set SSH password...")
        try:
            global_cred_lock.acquire()
            users = Collection("users")
            for user in users.find(sessionid = cherrypy.session.id):
                user.object['ssh password'] = b64decode(b64str)
                user.set()
        except Exception:
            add_message(traceback.format_exc())
        finally:
            global_cred_lock.release()
    
    @cherrypy.expose
    def set_mysql_password(self, b64str):
        add_message("credentials controller: set MySQL password...")
        try:
            global_cred_lock.acquire()
            users = Collection("users")
            for user in users.find(sessionid = cherrypy.session.id):
                user.object['mysql password'] = b64decode(b64str)
                user.set()
        except Exception:
            add_message(traceback.format_exc())
        finally:
            global_cred_lock.release()
    
    @cherrypy.expose
    def set_ssh_username(self, username):
        add_message("credentials controller: set SSH username: {0}".format(username))
        global_cred_lock.acquire()
        users = Collection("users")
        for user in users.find(sessionid = cherrypy.session.id):
            user.object['ssh username'] = username
            user.set()
        global_cred_lock.release()
    
    @cherrypy.expose
    def set_mysql_username(self, username):
        add_message("credentials controller: set MySQL username: {0}".format(username))
        global_cred_lock.acquire()
        users = Collection("users")
        for user in users.find(sessionid = cherrypy.session.id):
            user.object['mysql username'] = username
            user.set()
        global_cred_lock.release()