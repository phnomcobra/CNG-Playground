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
        self.nodes = [
       { "id" : "ajson1{0}".format(randrange(0, 9, 1)), "parent" : "#", "text" : "Simple root node{0}".format(randrange(0, 9, 1)) },
       { "id" : "ajson2", "parent" : "#", "text" : "Root node 2" },
       { "id" : "ajson3", "parent" : "ajson2", "text" : "Child 1" },
       { "id" : "ajson4{0}".format(randrange(0, 9, 1)), "parent" : "ajson2", "text" : "Child 2{0}".format(randrange(0, 9, 1)) },
    ]
        
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
        return json.dumps(self.nodes)
    
    @cherrypy.expose
    def ajax_move(self, id, parent):
        for node in self.nodes:
            if node["id"] == id:
                node["parent"] = parent
        return json.dumps({"id" : id, "parent" : parent})
    
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