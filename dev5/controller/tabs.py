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
        self.tabs = {}
    
    @cherrypy.expose
    def ajax_get_tabs(self):
        return json.dumps(self.tabs)
    
    @cherrypy.expose
    def ajax_get_tab(self, id):
        return json.dumps(self.tabs[id])
    
    @cherrypy.expose
    def ajax_close_tab(self, id):
        del self.tabs[id];
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_new_tab(self, id, route, label):
        self.tabs[id] = {};
        self.tabs[id]["route"] = route;
        self.tabs[id]["label"] = label;
        return json.dumps({})