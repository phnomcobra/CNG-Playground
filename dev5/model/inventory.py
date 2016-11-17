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
    node = {"id" : object.objuuid, 
            "parent" : object.object["parent"], 
            "text" : object.object["name"]}
    
    if "icon" in object.object:
        node["icon"] = object.object["icon"]
    
    nodes.append(node)

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
                "action" : {"method" : "ajax",
                            "route" : "inventory/ajax_create_container",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "new task" : {
                "label" : "New Task",
                "action" : {"method" : "ajax",
                            "route" : "inventory/ajax_create_task",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "new procedure" : {
                "label" : "New Procedure",
                "action" : {"method" : "ajax",
                            "route" : "inventory/ajax_create_procedure",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "new controller" : {
                "label" : "New Controller",
                "action" : {"method" : "ajax",
                            "route" : "inventory/ajax_create_controller",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "new rfc" : {
                "label" : "New RFC",
                "action" : {"method" : "ajax",
                            "route" : "inventory/ajax_create_rfc",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "ajax",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit container",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : container.objuuid}}
            }
        },
        "accepts" : ["container", "task"]
    }
    if parent_objuuid == "#":
        del container.object["context"]["delete"]
        container.object["icon"] = "images/tree_icon.png"
    else:
        parent = collection.get_object(parent_objuuid)
        parent.object["children"].append(container.objuuid)
        parent.set()
    
    container.set()

def create_task(parent_objuuid, name):
    collection = Collection("inventory")
    task = collection.get_object()
    task.object = {
        "type" : "task",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "body" : "",
        "icon" : "/images/task_icon.png",
        "context" : {
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "ajax",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : task.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit task",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : task.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(task.objuuid)
    parent.set()
    
    task.set()

def create_procedure(parent_objuuid, name):
    collection = Collection("inventory")
    procedure = collection.get_object()
    procedure.object = {
        "type" : "procedure",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "tasks" : [],
        "continue" : [],
        "title" : "",
        "description" : "",
        "rfcs" : [],
        "icon" : "/images/procedure_icon.png",
        "context" : {
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "ajax",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : procedure.objuuid}}
            },
            "edit description" : {
                "label" : "Edit Description",
                "action" : {"method" : "edit procedure description",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : procedure.objuuid}}
            },
            "edit tasks" : {
                "label" : "Edit Tasks",
                "action" : {"method" : "edit procedure tasks",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : procedure.objuuid}}
            },
            "edit rfcs" : {
                "label" : "Edit RFCs",
                "action" : {"method" : "edit procedure rfcs",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : procedure.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(procedure.objuuid)
    parent.set()
    
    procedure.set()

def create_rfc(parent_objuuid, name):
    collection = Collection("inventory")
    rfc = collection.get_object()
    rfc.object = {
        "type" : "rfc",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "title" : "",
        "description" : "",
        "poc name" : "",
        "poc email" : "",
        "poc phone" : "",
        "number" : "",
        "icon" : "/images/rfc_icon.png",
        "context" : {
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "ajax",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : rfc.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit rfc",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : rfc.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(rfc.objuuid)
    parent.set()
    
    rfc.set()

def create_controller(parent_objuuid, name):
    collection = Collection("inventory")
    controller = collection.get_object()
    controller.object = {
        "type" : "controller",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "icon" : "/images/controller_icon.png",
        "context" : {
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "ajax",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : controller.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(controller.objuuid)
    parent.set()
    
    controller.set()

def get(objuuid, **kargs):
    collection = Collection("inventory")
    object = collection.get_object(objuuid)
    
    result = {}
    for result_key, object_key in kargs.iteritems():
        try:
            result[result_key] = object.object[object_key]
        except Exception as e:
            result[result_key] = str(e)
    return result

def set(objuuid, **kargs):
    collection = Collection("inventory")
    object = collection.get_object(objuuid)
    
    for key, value in kargs.iteritems():
            object.object[key] = value
    
    object.set()

collection = Collection("inventory")
try:
    collection.create_attribute("parent", "['parent']")
except Exception:
    pass
    
if not len(collection.find(parent = "#")):
    create_container("#", "root")