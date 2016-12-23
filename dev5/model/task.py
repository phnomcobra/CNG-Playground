#!/usr/bin/python
################################################################################
# TASK
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/30/2016 Original construction
################################################################################

import traceback

from .document import Collection
from ..controller.messaging import add_message

from imp import new_module
from time import time

class TaskError:
    def __init__(self, uuid):
        self.output = ['<font color="red">'] + traceback.format_exc().split("\n") + ["</font>"]
        self.uuid = uuid
        self.status = 5 

    def execute(self, cli):
        return self.status

def execute(tskuuid, hstuuid, session):
    inventory = Collection("inventory")
    results = Collection("results")
    
    result = results.get_object()
    
    
    result.object['start'] = time()
        
    status_code_body = ""
    status_data = {}
    
    for status in inventory.find(type = "status"):
        try:
            status_code_body += "{0}=int('{1}')\n".format(status.object["alias"], status.object["code"])
            status_data[int(status.object["code"])] = status.object
        except Exception:
            add_message(traceback.format_exc())
    
    host = inventory.get_object(hstuuid)
    result.object['host'] = host.object
    
    tempmodule = new_module("tempmodule")
    
    try:
        exec inventory.get_object(host.object["console"]).object["body"] in tempmodule.__dict__
        cli = tempmodule.Console(session = session, host = host.object["host"])
        
        try:
            result.object['task'] = inventory.get_object(tskuuid).object
            exec status_code_body + inventory.get_object(tskuuid).object["body"] in tempmodule.__dict__
            task = tempmodule.Task()
            
            try:
                task.execute(cli)
            except Exception:
                task = TaskError(tskuuid)
                add_message(traceback.format_exc())
        except Exception:
            task = TaskError(tskuuid)
            add_message(traceback.format_exc())
    except Exception:
        task = TaskError(tskuuid)
        add_message(traceback.format_exc())
        
    result.object['output'] = task.output
    
    try:
        result.object['status'] = status_data[task.status]
    except Exception:
        add_message(traceback.format_exc())
        result.object['status'] = {"code" : task.status}
        
    result.object['stop'] = time()
        
    #for line in dir(tempmodule):
    #    print "module: ", line
    
    result.set()
    
    return result.object

def get_host_grid(tskuuid):
    collection = Collection("inventory")
    
    task = collection.get_object(tskuuid)
    
    grid_data = []
    
    for hstuuid in task.object["hosts"]:
        host = collection.get_object(hstuuid)
        
        if "type" in host.object:
            grid_data.append({"name" : host.object["name"], "host" : host.object["host"], "objuuid" : host.object["objuuid"]})
        else:
            add_message("host {0} is missing!".format(hstuuid))
            grid_data.append({"name" : "MISSING!", "host" : "?.?.?.?", "objuuid" : hstuuid})
        
    return grid_data