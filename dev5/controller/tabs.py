#!/usr/bin/python
################################################################################
# TABS
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/08/2016 Original construction
################################################################################

import cherrypy
import json

class Tabs(object):
    def __init__(self):
        self.tabs = []
    
    @cherrypy.expose
    def ajax_get_tabs(self):
        return json.dumps({"tabs" : self.tabs})
    
    @cherrypy.expose
    def ajax_close_tab(self, id):
        self.tabs.remove(id)
        return json.dumps({"tabs" : self.tabs})
    
    @cherrypy.expose
    def ajax_close_all(self):
        self.tabs = []
        return json.dumps({"tabs" : self.tabs})
    
    @cherrypy.expose
    def ajax_new_tab(self, id, action, name):
        if id not in self.tabs:
            self.tabs.append({"id" : id, "action" : action, "name" : name});
        return json.dumps({"tabs" : self.tabs})