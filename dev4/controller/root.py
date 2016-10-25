#!/usr/bin/python
################################################################################
# ROOT
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/16/2016 Original construction
################################################################################

import cherrypy
import json

from ..view.index import index_view
from random import randrange

class Root(object):
    def __init__(self):
        self.nodes = [
       { "id" : "ajson1{0}".format(randrange(0, 9, 1)), "parent" : "#", "text" : "Simple root node{0}".format(randrange(0, 9, 1)) },
       { "id" : "ajson2", "parent" : "#", "text" : "Root node 2" },
       { "id" : "ajson3", "parent" : "ajson2", "text" : "Child 1" },
       { "id" : "ajson4{0}".format(randrange(0, 9, 1)), "parent" : "ajson2", "text" : "Child 2{0}".format(randrange(0, 9, 1)) },
    ]
    
    def list_children(self, id, children = []):
        for node in self.nodes:
            if node["id"] == id:
                children.append(node)
        
        for node in self.nodes:
            if node["parent"] == id:
                self.list_children(node["id"], children)
        
        return children

    @cherrypy.expose
    def index(self):
        print "page load:"
        return index_view()

    @cherrypy.expose
    def ajax_roots(self, id):
        print "tree load:", id
        return json.dumps(self.nodes)
    
    @cherrypy.expose
    def ajax_move(self, id, parent):
        for node in self.nodes:
            if node["id"] == id:
                node["parent"] = parent
        return json.dumps({"id" : id, "parent" : parent})
    
    @cherrypy.expose
    def ajax_context(self, id):
        print "context load:", id
        return json.dumps({
                "Add": {
                    "label": "Add",
                    "option": "add",
                    },
                "Delete": {
                    "label": "Delete",
                    "option": "del",
                    }
                })
    
    @cherrypy.expose
    def ajax_context_select(self, id, option):
        print "context select:", id, option
        if option == "add":
            child = "{0}{1}{2}{3}".format(randrange(0, 9 ,1), randrange(0, 9 ,1), randrange(0, 9 ,1), randrange(0, 9 ,1))
            
            self.nodes.append({ "id" : child, "parent" : id, "text" : child })
        elif option == "del":
            for node in self.list_children(id):
                self.nodes.remove(node)
        
        return json.dumps({"id" : id, "option" : option})
    
    @cherrypy.expose
    def ajax_select(self, id):
        print "select:", id
        return json.dumps({"id" : id})