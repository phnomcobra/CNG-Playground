#!/usr/bin/python
################################################################################
# INVENTORY
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/07/2016 Original construction
# 04/11/2017 Moved object import logic here
################################################################################

import traceback

from .document import Collection
from .utils import sucky_uuid
from ..controller.messaging import add_message

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
            "new schedule" : {
                "label" : "New Schedule",
                "action" : {"method" : "create schedule",
                            "route" : "inventory/ajax_create_schedule",
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

def create_schedule(parent_objuuid, name = "New Schedule", objuuid = None):
    collection = Collection("inventory")
    schedule = collection.get_object(objuuid)
    schedule.object = {
        "type" : "schedule",
        "parent" : parent_objuuid,
        "children" : [],
        "name" : name,
        "description" : "",
        "body" : "",
        "enabled" : False,
        "minutes" : "",
        "hours" : "",
        "dayofmonth" : "",
        "dayofweek" : "",
        "year" : "",
        "icon" : "/images/schedule_icon.png",
        "context" : {
            "delete" : {
                "label" : "Delete",
                "action" : {"method" : "delete node",
                            "route" : "inventory/ajax_delete",
                            "params" : {"objuuid" : schedule.objuuid}}
            },
            "edit" : {
                "label" : "Edit",
                "action" : {"method" : "edit schedule",
                            "route" : "inventory/ajax_get_object",
                            "params" : {"objuuid" : schedule.objuuid}}
            },
            "copy" : {
                "label" : "Copy",
                "action" : {"method" : "copy node",
                            "route" : "inventory/ajax_copy_object",
                            "params" : {"objuuid" : schedule.objuuid}}
            },
            "create link" : {
                "label" : "Create Link",
                "action" : {"method" : "create link",
                            "route" : "inventory/ajax_create_link",
                            "params" : {"objuuid" : schedule.objuuid}}
            }
        },
        "accepts" : []
    }
    
    parent = collection.get_object(parent_objuuid)
    parent.object["children"].append(schedule.objuuid)
    parent.set()
    
    schedule.set()
    return schedule
    
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
                "label" : "Open",
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
                "label" : "Open",
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
            else:
                try:
                    object[key] = object[key].replace(find, replace)
                except Exception:
                    pass
    elif isinstance(object, list):
        for i, value in enumerate(object):
            if isinstance(value, dict) or isinstance(value, list):
                recstrrepl(object[i], find, replace)
            else:
                try:
                    object[i] = object[i].replace(find, replace)
                except Exception:
                    pass
    else:
        try:
            object = object.replace(find, replace)
        except Exception:
            pass

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
        elif current.object["type"] == "link":
            __get_dependencies(current.object["target"], objuuids, collection)
    
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

def get_required_objects_grid(objuuid):
    collection = Collection("inventory")
    
    required_objuuids = []
    
    object = collection.get_object(objuuid).object
    if "type" in object:
        if object["type"] == "host":
            required_objuuids.append(object["console"])
        elif object["type"] == "task":
            required_objuuids += object["hosts"]
        elif object["type"] == "procedure":
            required_objuuids += object["hosts"]
            required_objuuids += object["rfcs"]
            required_objuuids += object["tasks"]
        elif object["type"] == "controller":
            required_objuuids += object["hosts"]
            required_objuuids += object["procedures"]
    
    grid_data = []
    
    for objuuid in required_objuuids:
        object = collection.get_object(objuuid).object
        
        if "type" in object:
            grid_data.append({"name" : object["name"], "type" : object["type"], "objuuid" : object["objuuid"]})
        else:
            add_message("object {0} is missing!".format(object["objuuid"]))
            grid_data.append({"name" : "MISSING!", "type" : "???????", "objuuid" : object["objuuid"]})
        
    return grid_data

def get_provided_objects_grid(objuuid):
    collection = Collection("inventory")
    
    required_objuuids = []
    
    object = collection.get_object(objuuid).object
    if "type" in object:
        if object["type"] == "console":
            for hstuuid in collection.find_objuuids(type = "host"):
                if collection.get_object(hstuuid).object["console"] == objuuid:
                    required_objuuids.append(hstuuid)

        elif object["type"] == "host":
            for tskuuid in collection.find_objuuids(type = "task"):
                if objuuid in collection.get_object(tskuuid).object["hosts"]:
                    required_objuuids.append(tskuuid)
            
            for prcuuid in collection.find_objuuids(type = "procedure"):
                if objuuid in collection.get_object(prcuuid).object["hosts"]:
                    required_objuuids.append(prcuuid)
            
            for ctruuid in collection.find_objuuids(type = "controller"):
                if objuuid in collection.get_object(ctruuid).object["hosts"]:
                    required_objuuids.append(ctruuid)

        elif object["type"] == "rfc":
            for prcuuid in collection.find_objuuids(type = "procedure"):
                if objuuid in collection.get_object(prcuuid).object["rfcs"]:
                    required_objuuids.append(prcuuid)

        elif object["type"] == "task":
            for prcuuid in collection.find_objuuids(type = "procedure"):
                if objuuid in collection.get_object(prcuuid).object["tasks"]:
                    required_objuuids.append(prcuuid)
                    
        elif object["type"] == "procedure":
            for ctruuid in collection.find_objuuids(type = "controller"):
                if objuuid in collection.get_object(ctruuid).object["procedures"]:
                    required_objuuids.append(ctruuid)
    
    grid_data = []
    
    for objuuid in required_objuuids:
        object = collection.get_object(objuuid).object
        
        if "type" in object:
            grid_data.append({"name" : object["name"], "type" : object["type"], "objuuid" : object["objuuid"]})
        else:
            add_message("object {0} is missing!".format(object["objuuid"]))
            grid_data.append({"name" : "MISSING!", "type" : "???????", "objuuid" : object["objuuid"]})
        
    return grid_data

def import_objects(objects):
    collection = Collection("inventory")
            
    container = create_container("#", "Imported Objects")
    
    objuuids = collection.list_objuuids()    
    for objuuid, object in objects.iteritems():
        try:
            current = collection.get_object(objuuid)
            
            if "parent" in current.object:
                if current.object["parent"] in objuuids:
                    parent = collection.get_object(current.object["parent"])
                    
                    if "children" in parent.object:
                        parent.object["children"].remove(objuuid)
                        parent.set()
                
            if "children" in current.object:
                old_children = current.object["children"]
                current.object = object
                        
                for child in old_children:
                    if child not in current.object["children"]:
                        current.object["children"].append(child)
            else:
                current.object = object
            
            if "parent" in current.object:
                if current.object["parent"] in objuuids:
                    parent = collection.get_object(current.object["parent"])
                    
                    if "children" in parent.object:
                        if objuuid not in parent.object["children"]:
                            parent.object["children"].append(objuuid)
                            parent.set()
                        
            current.set()
            
            add_message("imported: {0}, type: {1}, name: {2}".format(objuuid, object["type"], object["name"]))
        except Exception:
            add_message(traceback.format_exc())
            
    objuuids = collection.list_objuuids()
    for objuuid in objuuids:
        current = collection.get_object(objuuid)
        if "parent" in current.object:
            if current.object["parent"] not in objuuids and \
               current.object["parent"] != "#":
                current.object["parent"] = container.objuuid
                container.object["children"].append(objuuid)
                current.set()
            elif current.object["parent"] != "#":
                parent = collection.get_object(current.object["parent"])
                if current.objuuid not in parent.object["children"]:
                    parent.object["children"].append(current.objuuid)
                    parent.set()
            
    if len(container.object["children"]) > 0:
        container.set()
    else:
        container.destroy()
    
collection = Collection("inventory")
collection.create_attribute("parent", "['parent']")
collection.create_attribute("type", "['type']")
collection.create_attribute("name", "['name']")
    
if not len(collection.find(parent = "#")):
    create_container("#", "root")
