#!/usr/bin/python
################################################################################
# INVENTORY
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/16/2016 Original construction
################################################################################

import cherrypy
import json

from random import randrange

class Inventory(object):
    def __init__(self):
        self.nodes = [{ "id" : "root", "parent" : "#", "text" : "root"}]
        
        self.tabs = {}
    
    def list_children(self, id, children = []):
        for node in self.nodes:
            if node["id"] == id:
                children.append(node)
        
        for node in self.nodes:
            if node["parent"] == id:
                self.list_children(node["id"], children)
        
        return children

    @cherrypy.expose
    def ajax_roots(self, id):
        for node in self.nodes:
            print node
        print ""
        return json.dumps(self.nodes)
    
    @cherrypy.expose
    def ajax_move(self, id, parent, position):
        for node in self.nodes:
            if node["id"] == id:
                node["parent"] = parent
                print "inside position", id, parent, position
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_context(self, id):
        return json.dumps({
                "Add": {
                    "label": "Add",
                    "option": "add",
                    },
                "Delete": {
                    "label": "Delete",
                    "option": "del",
                    },
                "Edit": {
                    "label": "Edit",
                    "option": "edit",
                    }
                })
    
    @cherrypy.expose
    def ajax_context_select(self, id, option):
        if option == "add":
            child = "{0}{1}{2}{3}".format(randrange(0, 9 ,1), randrange(0, 9 ,1), randrange(0, 9 ,1), randrange(0, 9 ,1))
            
            self.nodes.append({ "id" : child, "parent" : id, "text" : child })
            return json.dumps({})
        elif option == "del":
            for node in self.list_children(id):
                self.nodes.remove(node)
            return json.dumps({})
        elif option == "edit":
            self.tabs["tab{0}".format(id)] = {"route" : "get_dummy", "label":"edit {0}".format(id)}
            return json.dumps({})
    
    @cherrypy.expose
    def ajax_get_tabs(self):
        return json.dumps(self.tabs)
    
    @cherrypy.expose
    def ajax_close_tab(self, item):
        del self.tabs[item];
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_select(self, id):
        return json.dumps({})