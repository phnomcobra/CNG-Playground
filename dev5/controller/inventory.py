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
from ..model.document import Collection, Object

class Inventory(object):
    def __init__(self):
        collection = Collection("inventory")
        try:
            collection.create_attribute("type", "['type']")
        except Exception:
            pass
        
        try:
            collection.create_attribute("parent", "['parent']")
        except Exception:
            pass
        
        try:
            collection.create_attribute("objuuid", "['objuuid']")
        except Exception:
            pass
        
        root_objects = collection.find(parent = "#")
        if not len(root_objects):
            root_object = collection.get_object()
            root_object.object["type"] = "container"
            root_object.object["parent"] = '#'
            root_object.object["children"] = []
            root_object.object["name"] = "root"
        
        self.tabs = {}
    
    def get_child_nodes(self, nodes, object):
        nodes.append({"id" : object.objuuid, 
                      "parent" : object.object["parent"], 
                      "text" : object.object["name"]})

        for objuuid in object.object["children"]:
            nodes = self.get_child_nodes(nodes, Object(object.coluuid, objuuid))
        
        return nodes
    
    @cherrypy.expose
    def ajax_roots(self, id):
        nodes = []
        collection = Collection("inventory")
        
        for object in collection.find(parent = id):
            nodes = self.get_child_nodes(nodes, object)
        
        return json.dumps(nodes)
    
    @cherrypy.expose
    def ajax_move(self, id, parent):
        collection = Collection("inventory")

        parent_object = Object(collection.coluuid, Object(collection.coluuid, id).object["parent"])
        parent_object.object["children"].remove(id)
        parent_object.set()

        current_object = collection.get_object(id)
        current_object.object["parent"] = parent
        current_object.set()

        parent_object = Object(collection.coluuid, Object(collection.coluuid, id).object["parent"])
        parent_object.object["children"].append(id)
        parent_object.set()

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
        collection = Collection("inventory")
        if option == "add":
            new_object = collection.get_object()
            new_object.object["type"] = "container"
            new_object.object["parent"] = id
            new_object.object["children"] = []
            new_object.object["name"] = "child: " + new_object.objuuid[:8]
            
            current_object = Object(collection.coluuid, id)
            current_object.object["children"].append(new_object.objuuid)
            
            return json.dumps({})
        elif option == "del":
            parent_object = Object(collection.coluuid, Object(collection.coluuid, id).object["parent"])
            parent_object.object["children"].remove(id)
            parent_object.set()

            nodes = []
            for node in self.get_child_nodes(nodes, Object(collection.coluuid, id)):
                current_object = Object(collection.coluuid, node["id"])
                current_object.destroy()

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