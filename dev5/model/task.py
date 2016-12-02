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
    collection = Collection("inventory")
    
    result = {}
    
    result['start'] = time()
        
    status_code_body = ""
    status_data = {}
    
    for status in collection.find(type = "status"):
        try:
            status_code_body += "{0}=int('{1}')\n".format(status.object["alias"], status.object["code"])
            status_data[int(status.object["code"])] = status.object
        except Exception:
            print traceback.format_exc()
    
    host = collection.get_object(hstuuid)
    
    tempmodule = new_module("tempmodule")
    
    try:
        exec collection.get_object(host.object["console"]).object["body"] in tempmodule.__dict__
        cli = tempmodule.Console(session = session, host = host.object["host"])
        
        result['host'] = host.object
        
        try:
            exec status_code_body + collection.get_object(tskuuid).object["body"] in tempmodule.__dict__
            task = tempmodule.Task()
            
            try:
                task.execute(cli)
            except Exception:
                task = TaskError(tskuuid)
        except Exception:
            task = TaskError(tskuuid)
    except Exception:
        task = TaskError(tskuuid)
        
    result['output'] = task.output
    
    try:
        result['status'] = status_data[task.status]
    except Exception:
        result['status'] = {"code" : task.status}
        
    result['stop'] = time()
        
    #for line in dir(tempmodule):
    #    print "module: ", line
    
    return result

def get_host_grid(tskuuid):
    collection = Collection("inventory")
    
    task = collection.get_object(tskuuid)
    
    grid_data = []
    
    for hstuuid in task.object["hosts"]:
        host = collection.get_object(hstuuid)
        
        grid_data.append({"name" : host.object["name"], "host" : host.object["host"], "objuuid" : host.object["objuuid"]})
        
    return grid_data
