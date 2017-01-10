#!/usr/bin/python
################################################################################
# AUTH
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 01/03/2017 Original construction
################################################################################

import cherrypy
import json
import traceback

from ..model.document import Collection
from ..model.auth import create_user, get_users_grid
from .messaging import add_message
from ..view.auth import login_view, admin_view

SESSION_KEY = '_cp_username'

def check_credentials(username, password):
    users = Collection("users")
    
    for user in users.find(name = username):
        if user.object["enabled"] == 'false':
            return "User {0} is disabled!".format(username)
        if user.object["password"] == password:
            return None
        else:
            return "Incorrect password!"
    return "User {0} does not exist!".format(username)

def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("/auth/login")
        else:
            raise cherrypy.HTTPRedirect("/auth/login")
    
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate

def member_of(groupname):
    def check():
        users = Collection("users")
    
        for user in users.find(name = cherrypy.request.login):
            if user.object["role"] == groupname:
                return True
            else:
                return False
        return False

    return check

def name_is(reqd_username):
    return lambda: reqd_username == cherrypy.request.login

# These might be handy

def any_of(*conditions):
    """Returns True if any of the conditions match"""
    def check():
        for c in conditions:
            if c():
                return True
        return False
    return check

# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
def all_of(*conditions):
    """Returns True if all of the conditions match"""
    def check():
        for c in conditions:
            if not c():
                return False
        return True
    return check

class Auth(object):
    def on_login(self, username):
        """Called on successful login"""
    
    def on_logout(self, username):
        """Called on logout"""
    
    @cherrypy.expose
    @require(member_of("admin"))
    def admin(self):
        return admin_view()
    
    @cherrypy.expose
    def login(self, username=None, password=None, from_page="/"):
        if username is None or password is None:
            return login_view("", from_page=from_page)
        
        error_msg = check_credentials(username, password)
        if error_msg:
            return login_view(username, error_msg, from_page)
        else:
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            self.on_login(username)
            raise cherrypy.HTTPRedirect(from_page or "/")
    
    @cherrypy.expose
    def logout(self, from_page="/"):
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page or "/")

    @cherrypy.expose
    def ajax_get_users_grid(self):
        add_message("auth controller: get users grid")
        try:
            return json.dumps(get_users_grid())
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_create_user(self, name):
        add_message("auth controller: create user: {0}".format(name))
        try:
            return json.dumps(create_user(name).object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_delete(self, objuuid):
        add_message("auth controller: delete user object: {0}".format(objuuid))
        try:
            Collection("users").get_object(objuuid).destroy()
            return json.dumps({"id" : objuuid})
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_get_object(self, objuuid):
        add_message("auth controller: get user object...")
        try:
            collection = Collection("users")
            object = collection.get_object(objuuid).object
            add_message("auth controller: get: {0}, name: {1}".format(objuuid, object["name"]))
            return json.dumps(object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_post_object(self):
        add_message("auth controller: post user object...")
        
        try:
            cl = cherrypy.request.headers['Content-Length']
            object = json.loads(cherrypy.request.body.read(int(cl)))
        
            collection = Collection("users")
            current = collection.get_object(object["objuuid"])
            current.object = object
            current.set()
            
            add_message("auth controller: set: {0}, name: {1}".format(object["objuuid"], object["name"]))
        
            return json.dumps(current.object)
        except Exception:
            add_message(traceback.format_exc())