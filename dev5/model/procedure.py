#!/usr/bin/python
################################################################################
# PROCEDURE
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/22/2016 Original construction
################################################################################

import traceback

from time import time
from imp import new_module

from .document import Collection
from ..controller.flags import touch_flag
from ..controller.messaging import add_message
from .task import TaskError

class TaskError:
    def __init__(self, uuid):
        self.output = ['<font color="red">'] + traceback.format_exc().split("\n") + ["</font>"]
        self.uuid = uuid
        self.status = 5 

    def execute(self, cli):
        return self.status

def get_task_grid(prcuuid):
    collection = Collection("inventory")
    
    procedure = collection.get_object(prcuuid)
    
    grid_data = []
    
    for tskuuid in procedure.object["tasks"]:
        task = collection.get_object(tskuuid)
        
        if "type" in task.object:
            grid_data.append({"name" : task.object["name"], "objuuid" : task.object["objuuid"]})
        else:
            add_message("task {0} is missing!".format(tskuuid))
            grid_data.append({"name" : "MISSING!", "objuuid" : tskuuid})
        
    return grid_data

def get_related_procedure_grid(prcuuid):
    collection = Collection("inventory")
    
    procedure = collection.get_object(prcuuid)
    
    grid_data = []
    
    for prcuuid in procedure.object["procedures"]:
        related_procedure = collection.get_object(prcuuid)
        
        grid_data.append({"name" : related_procedure.object["name"], "objuuid" : related_procedure.object["objuuid"]})
        
        if "type" in related_procedure.object:
            grid_data.append({"name" : related_procedure.object["name"], "objuuid" : related_procedure.object["objuuid"]})
        else:
            add_message("procedure {0} is missing!".format(prcuuid))
            grid_data.append({"name" : "MISSING!", "objuuid" : prcuuid})
        
    return grid_data

def get_related_procedures(prcuuid):
    collection = Collection("inventory")
    
    procedures = []
    for rlpuuid in collection.get_object(prcuuid).object["procedures"]:
        related_procedure = collection.get_object(rlpuuid)
        
        if "type" in related_procedure.object:
            procedures.append(related_procedure.object)
        
    return procedures

def get_host_grid(prcuuid):
    collection = Collection("inventory")
    
    procedure = collection.get_object(prcuuid)
    
    grid_data = []
    
    for hstuuid in procedure.object["hosts"]:
        host = collection.get_object(hstuuid)
        
        if "type" in host.object:
            grid_data.append({"name" : host.object["name"], "host" : host.object["host"], "objuuid" : host.object["objuuid"]})
        else:
            add_message("host {0} is missing!".format(hstuuid))
            grid_data.append({"name" : "MISSING!", "host" : "?.?.?.?", "objuuid" : hstuuid})
        
    return grid_data

def execute(prcuuid, hstuuid, session):
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
    result.object['procedure'] = inventory.get_object(prcuuid).object
        
    tempmodule = new_module("tempmodule")
    
    winning_status = None
    continue_procedure = True
    
    result.object['tasks'] = []
    
    result.object['rfcs'] = []
    for rfcuuid in inventory.get_object(prcuuid).object["rfcs"]:
        result.object['rfcs'].append(inventory.get_object(rfcuuid).object)
    
    try:
        try:
            exec inventory.get_object(host.object["console"]).object["body"] in tempmodule.__dict__
            cli = tempmodule.Console(session = session, host = host.object["host"])
        except Exception:
            add_message(traceback.format_exc())
        
        for tskuuid in inventory.get_object(prcuuid).object["tasks"]:
            task_result = inventory.get_object(tskuuid).object
            
            try:
                exec status_code_body + inventory.get_object(tskuuid).object["body"] in tempmodule.__dict__
                task = tempmodule.Task()
                
                if continue_procedure:
                    task_result["start"] = time()
                    
                    try:
                        task.execute(cli)
                    except Exception:
                        task = TaskError(tskuuid)
                        add_message(traceback.format_exc())
                    
                    task_result["stop"] = time()
            except Exception:
                task = TaskError(tskuuid)
                add_message(traceback.format_exc())
            
            task_result["output"] = task.output
            try:
                task_result["status"] = status_data[task.status]
                try:
                    if not inventory.get_object(prcuuid).object["continue {0}".format(task.status)]:
                        continue_procedure = False
                except Exception:
                    continue_procedure = False
                    add_message(traceback.format_exc())
            except Exception:
                task_result['status'] = {"code" : task.status}
                continue_procedure = False
                add_message(traceback.format_exc())
            result.object['tasks'].append(task_result)
            
            if winning_status == None:
                winning_status = task.status
                result.object['status'] = task_result['status']
            elif task.status < winning_status:
                winning_status = task.status
                result.object['status'] = task_result['status']
        
    except Exception:
        add_message(traceback.format_exc())
        
    result.object['stop'] = time()

    touch_flag("results")
    
    #for line in dir(tempmodule):
    #    print "module: ", line
    
    result.set()
    
    return result.object
