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

import traceback

from .document import Collection
from .utils import sucky_uuid

def __get_child_nodes(nodes, object, collection):
    try:
        node = {"id" : object.objuuid, 
                "parent" : object.object["parent"], 
                "text" : object.object["name"],
                "type" : object.object["type"]}
    
        if "icon" in object.object:
            node["icon"] = object.object["icon"]
    
        nodes.append(node)

        for objuuid in object.object["children"]:
            nodes = __get_child_nodes(nodes, collection.get_object(objuuid), collection)
    except Exception:
        print traceback.format_exc()
        print object.object
 
    return nodes
    
def get_child_nodes(objuuid):
    nodes = []
    collection = Collection("inventory")
        
    for object in collection.find(parent = objuuid):
        nodes = __get_child_nodes(nodes, object, collection)
    
    return nodes
    
def set_parent_objuuid(objuuid, parent_objuuid):
    if objuuid == parent_objuuid:
        print "UUID collision detected while attempting to move",
        print objuuid
        return None
        
    collection = Collection("inventory")

    current = collection.get_object(objuuid)
    
    if current.object["parent"] != '#':
        try:
            parent = collection.get_object(current.object["parent"])
            parent.object["children"].remove(objuuid)
            parent.set()
        except Exception:
            print traceback.format_exc()

    current.object["parent"] = parent_objuuid
    current.set()
    
    if parent_objuuid != '#':
        new_parent = collection.get_object(parent_objuuid)
        new_parent.object["children"].append(objuuid)
        new_parent.set()
    
def delete_node(objuuid):
    collection = Collection("inventory")
    
    if collection.get_object(objuuid).object["parent"] != "#":
        parent = collection.get_object(collection.get_object(objuuid).object["parent"])
        parent.object["children"].remove(objuuid)
        parent.set()
    
    for node in get_child_nodes(objuuid):
        current = collection.get_object(node["id"])
        current.destroy()
    
    collection.get_object(objuuid).destroy()
    
def get_context_menu(objuuid):
    return Collection("inventory").get_object(objuuid).object["context"]

def create_container(parent_objuuid, name = "New Container", objuuid = None):
    collection = Collection("inventory")
    container = collection.get_object(objuuid)
    container.object = {
        "type" : "container",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "context" : {
            "new container" : {
                "label" : "New Container",
                "action" : {"method" : "create container",
                            "route" : "inventory/ajax_create_container",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "new task" : {
                "label" : "New Task",
                "action" : {"method" : "create task",
                            "route" : "inventory/ajax_create_task",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "new procedure" : {
                "label" : "New Procedure",
                "action" : {"method" : "create procedure",
                            "route" : "inventory/ajax_create_procedure",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "new controller" : {
                "label" : "New Controller",
                "action" : {"method" : "create controller",
                            "route" : "inventory/ajax_create_controller",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "new rfc" : {
                "label" : "New RFC",
                "action" : {"method" : "create rfc",
                            "route" : "inventory/ajax_create_rfc",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "new status" : {
                "label" : "New Status Code",
                "action" : {"method" : "create status",
                            "route" : "inventory/ajax_create_status_code",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "new host" : {
                "label" : "New Host",
                "action" : {"method" : "create host",
                            "route" : "inventory/ajax_create_host",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "new console" : {
                "label" : "New Console",
                "action" : {"method" : "create console",
                            "route" : "inventory/ajax_create_console",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "delete node",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit container",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : container.objuuid}}
            },
            "copy" : {
                "label" : "Copy",
                "action" : {"method" : "copy node",
                            "route" : "inventory/ajax_copy_object",
                            "params" : {"objuuid" : container.objuuid}}
            }
        },
        "accepts" : ["container", "task"]
    }
    if parent_objuuid == "#":
        #del container.object["context"]["delete"]
        container.object["icon"] = "images/tree_icon.png"
    else:
        parent = collection.get_object(parent_objuuid)
        parent.object["children"].append(container.objuuid)
        parent.set()
    
    container.set()
    return container

def create_task(parent_objuuid, name = "New Task", objuuid = None):
    collection = Collection("inventory")
    task = collection.get_object(objuuid)
    task.object = {
        "type" : "task",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "body" : "",
        "hosts" : [],
        "icon" : "/images/task_icon.png",
        "context" : {
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "delete node",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : task.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit task",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : task.objuuid}}
            },
            "edit hosts" : {
                "label" : "Edit Hosts",
                "action" : {"method" : "edit task hosts",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : task.objuuid}}
            },
            "run" : {
                "label" : "Run",
                "action" : {"method" : "run task",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : task.objuuid}}
            },
            "copy" : {
                "label" : "Copy",
                "action" : {"method" : "copy node",
                            "route" : "inventory/ajax_copy_object",
                            "params" : {"objuuid" : task.objuuid}}
            },
            "create link" : {
                "label" : "Create Link",
                "action" : {"method" : "create link",
                            "route" : "inventory/ajax_create_link",
                            "params" : {"objuuid" : task.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(task.objuuid)
    parent.set()
    
    task.set()
    return task

def create_procedure(parent_objuuid, name = "New Procedure", objuuid = None):
    collection = Collection("inventory")
    procedure = collection.get_object(objuuid)
    procedure.object = {
        "type" : "procedure",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "tasks" : [],
        "title" : "",
        "description" : "",
        "rfcs" : [],
        "hosts" : [],
        "icon" : "/images/procedure_icon.png",
        "context" : {
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "delete node",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : procedure.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit procedure",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : procedure.objuuid}}
            },
            "run" : {
                "label" : "Run",
                "action" : {"method" : "run procedure",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : procedure.objuuid}}
            },
            "copy" : {
                "label" : "Copy",
                "action" : {"method" : "copy node",
                            "route" : "inventory/ajax_copy_object",
                            "params" : {"objuuid" : procedure.objuuid}}
            },
            "create link" : {
                "label" : "Create Link",
                "action" : {"method" : "create link",
                            "route" : "inventory/ajax_create_link",
                            "params" : {"objuuid" : procedure.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(procedure.objuuid)
    parent.set()
    
    procedure.set()
    return procedure

def create_rfc(parent_objuuid, name = "New RFC", objuuid = None):
    collection = Collection("inventory")
    rfc = collection.get_object(objuuid)
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
                "action" : {"method" : "delete node",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : rfc.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit rfc",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : rfc.objuuid}}
            },
            "copy" : {
                "label" : "Copy",
                "action" : {"method" : "copy node",
                            "route" : "inventory/ajax_copy_object",
                            "params" : {"objuuid" : rfc.objuuid}}
            },
            "create link" : {
                "label" : "Create Link",
                "action" : {"method" : "create link",
                            "route" : "inventory/ajax_create_link",
                            "params" : {"objuuid" : rfc.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(rfc.objuuid)
    parent.set()
    
    rfc.set()
    return rfc

def create_controller(parent_objuuid, name = "New Controller", objuuid = None):
    collection = Collection("inventory")
    controller = collection.get_object(objuuid)
    controller.object = {
        "type" : "controller",
        "parent" : parent_objuuid,
        "children" : [],
        "hosts" : [],
        "procedures" : [],
        "name" : name,
        "icon" : "/images/controller_icon.png",
        "context" : {
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "delete node",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : controller.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit controller",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : controller.objuuid}}
            },
            "run" : {
                "label" : "Run",
                "action" : {"method" : "run controller",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : controller.objuuid}}
            },
            "copy" : {
                "label" : "Copy",
                "action" : {"method" : "copy node",
                            "route" : "inventory/ajax_copy_object",
                            "params" : {"objuuid" : controller.objuuid}}
            },
            "create link" : {
                "label" : "Create Link",
                "action" : {"method" : "create link",
                            "route" : "inventory/ajax_create_link",
                            "params" : {"objuuid" : controller.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(controller.objuuid)
    parent.set()
    
    controller.set()
    return controller

def create_status_code(parent_objuuid, name = "New Status Code", objuuid = None):
    collection = Collection("inventory")
    status = collection.get_object(objuuid)
    status.object = {
        "type" : "status",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "alias" : "STATUS_{0}".format(str(name).upper()),
        "code" : 0,
        "abbreviation" : name,
        "cfg" : "000000",
        "cbg" : "FFFFFF",
        "sfg" : "000000",
        "sbg" : "999999",
        "icon" : "/images/status_icon.png",
        "context" : {
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "delete node",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : status.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit status code",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : status.objuuid}}
            },
            "copy" : {
                "label" : "Copy",
                "action" : {"method" : "copy node",
                            "route" : "inventory/ajax_copy_object",
                            "params" : {"objuuid" : status.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(status.objuuid)
    parent.set()
    
    status.set()
    return status

def create_host(parent_objuuid, name = "New Host", objuuid = None):
    collection = Collection("inventory")
    host = collection.get_object(objuuid)
    host.object = {
        "type" : "host",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "host" : "",
        "icon" : "/images/host_icon.png",
        "console" : None,
        "context" : {
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "delete node",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : host.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit host",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : host.objuuid}}
            },
            "terminal" : {
                "label" : "Terminal",
                "action" : {"method" : "create terminal",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : host.objuuid}}
            },
            "copy" : {
                "label" : "Copy",
                "action" : {"method" : "copy node",
                            "route" : "inventory/ajax_copy_object",
                            "params" : {"objuuid" : host.objuuid}}
            },
            "create link" : {
                "label" : "Create Link",
                "action" : {"method" : "create link",
                            "route" : "inventory/ajax_create_link",
                            "params" : {"objuuid" : host.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(host.objuuid)
    parent.set()
    
    host.set()
    return host

def create_console(parent_objuuid, name = "New Console", objuuid = None):
    collection = Collection("inventory")
    console = collection.get_object(objuuid)
    console.object = {
        "type" : "console",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "body" : "",
        "icon" : "/images/console_icon.png",
        "context" : {
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "delete node",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : console.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit console",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : console.objuuid}}
            },
            "copy" : {
                "label" : "Copy",
                "action" : {"method" : "copy node",
                            "route" : "inventory/ajax_copy_object",
                            "params" : {"objuuid" : console.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(console.objuuid)
    parent.set()
    
    console.set()
    return console

def create_link(target_objuuid, parent_objuuid = None, objuuid = None):
    collection = Collection("inventory")
    
    target = collection.get_object(target_objuuid)
    
    if parent_objuuid == None:
        parent_objuuid = target.object["parent"]
    
    link = collection.get_object(objuuid)
    link.object = {
        "type" : "link",
        "target" : target_objuuid,
        "target type" : target.object["type"],
        "parent" : parent_objuuid,
        "children" : [],
        "name" : target.object["name"],
        "icon" : "/images/link_icon.png",
        "context" : target.object["context"],
        "accepts" : []
    }
    
    link.object["context"]["delete"] = {
        "label" : "Delete Link",
        "action" : {
            "method" : "delete node",
            "route" : "inventory/ajax_delete",
            "params" : {"objuuid" : link.objuuid}
        }
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(link.objuuid)
    parent.set()
    
    link.set()
    return link

def recstrrepl(object, find, replace):
    if isinstance(object, dict):
        for key, value in object.iteritems():
            if isinstance(value, dict) or isinstance(value, list):
                recstrrepl(object[key], find, replace)
            elif isinstance(value, str):
                if object[key] == find:
                    object[key] = replace
    elif isinstance(object, list):
        for i, value in enumerate(object):
            if isinstance(value, dict) or isinstance(value, list):
                recstrrepl(object[i], find, replace)
            elif isinstance(value, str):
                if object[i] == find:
                    object[i] = replace
    elif isinstance(object, str):
        if object == find:
            object = replace

def copy_object(objuuid):
    collection = Collection("inventory")
    current_object = collection.get_object(objuuid)
    
    new_object = collection.get_object()
    new_objuuid = new_object.object["objuuid"]
    
    new_object.object = current_object.object
    new_object.object["children"] = []
    recstrrepl(new_object.object, objuuid, new_objuuid)
    new_object.object["name"] = new_object.object["name"] + " (Copy)"
    
    parent = collection.get_object(new_object.object["parent"])
    parent.object["children"].append(new_objuuid)
    parent.set()
    
    new_object.set()
    return new_object
    

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

def __get_dependencies(objuuid, objuuids, collection):
    if objuuid not in objuuids:
        objuuids.append(objuuid)
    
    current = collection.get_object(objuuid)
    
    if "type" in current.object:
        if current.object["type"] == "controller":
            for hstuuid in current.object["hosts"]:
                __get_dependencies(hstuuid, objuuids, collection)
        
            for prcuuid in current.object["procedures"]:
                __get_dependencies(prcuuid, objuuids, collection)
        elif current.object["type"] == "procedure":
            for hstuuid in current.object["hosts"]:
                __get_dependencies(hstuuid, objuuids, collection)
        
            for tskuuid in current.object["tasks"]:
                __get_dependencies(tskuuid, objuuids, collection)
        
            for rfcuuid in current.object["rfcs"]:
                __get_dependencies(rfcuuid, objuuids, collection)
        elif current.object["type"] == "task":
            for hstuuid in current.object["hosts"]:
                __get_dependencies(hstuuid, objuuids, collection)
        elif current.object["type"] == "host":
            if current.object["console"] != None:
                __get_dependencies(current.object["console"], objuuids, collection)
    
def get_dependencies(selected_objuuids):
    collection = Collection("inventory")
    objuuids = []
    
    for objuuid in selected_objuuids:
        __get_dependencies(objuuid, objuuids, collection)
    
    for status in collection.find(type = "status"):
        objuuids.append(status.objuuid)
    
    return objuuids
    
def get_status_objects():
    collection = Collection("inventory")
    
    status_objects = []
    
    for object in collection.find(type = "status"):
        status_objects.append(object.object)
        
    return status_objects
    
collection = Collection("inventory")
collection.create_attribute("parent", "['parent']")
collection.create_attribute("type", "['type']")
collection.create_attribute("name", "['name']")
    
if not len(collection.find(parent = "#")):
    create_container("#", "root")
