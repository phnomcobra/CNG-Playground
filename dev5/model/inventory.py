#!/usr/bin/python
################################################################################
# INVENTORY
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/07/2016 Original construction
################################################################################

from .document import Collection
from .utils import sucky_uuid

def __get_child_nodes(nodes, object, collection):
    nodes.append({"id" : object.objuuid, 
                  "parent" : object.object["parent"], 
                  "text" : object.object["name"]})

    for objuuid in object.object["children"]:
        nodes = __get_child_nodes(nodes, collection.get_object(objuuid), collection)
 
    return nodes
    
def get_child_nodes(objuuid):
    nodes = []
    collection = Collection("inventory")
        
    for object in collection.find(parent = objuuid):
        nodes = __get_child_nodes(nodes, object, collection)
    
    return nodes
    
def set_parent_objuuid(objuuid, parent_objuuid):
    collection = Collection("inventory")

    new_parent = collection.get_object(parent_objuuid)
    current = collection.get_object(objuuid)
    parent = collection.get_object(current.object["parent"])
        
    parent.object["children"].remove(objuuid)
    parent.set()

    current.object["parent"] = parent_objuuid
    current.set()

    new_parent.object["children"].append(objuuid)
    new_parent.set()
    
def delete_node(objuuid):
    collection = Collection("inventory")
    
    parent = collection.get_object(collection.get_object(objuuid).object["parent"])
    parent.object["children"].remove(objuuid)
    parent.set()
    
    for node in get_child_nodes(objuuid):
        current = collection.get_object(node["id"])
        current.destroy()
    
    collection.get_object(objuuid).destroy()
    
def get_context_menu(objuuid):
    return Collection("inventory").get_object(objuuid).object["context"]

def create_container(parent_objuuid, name):
    collection = Collection("inventory")
    container = collection.get_object()
    container.object = {
        "type" : "container",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "context" : {
            "new container" : {
                "label" : "New Container",
                "route" : "inventory/ajax_create_container",
                "params" : {"id" : container.objuuid}
            },
            "delete" : {
                "label" : "Delete",
                "route" : "inventory/ajax_delete",
                "params" : {"id" : container.objuuid}
            }
        },
        "accepts" : ["container", "task"]
    }
    if parent_objuuid == "#":
        del container.object["context"]["delete"]
    else:
        parent = collection.get_object(parent_objuuid)
        parent.object["children"].append(container.objuuid)
        parent.set()
    
    container.set()

collection = Collection("inventory")
try:
    collection.create_attribute("parent", "['parent']")
except Exception:
    pass

if not len(collection.find(parent = "#")):
    create_container("#", "root")