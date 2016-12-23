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

MAX_JOBS = 10

import traceback

from threading import Lock, Thread
from time import time, sleep
from imp import new_module

from .document import Collection
from .ramdocument import Collection as RAMCollection
from .utils import sucky_uuid
from ..controller.flags import touch_flag
from ..controller.messaging import add_message

global global_jobs
global global_jobs_lock
global_jobs = {}
global_job_lock = Lock()

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

def set_job(key, value):
    global_job_lock.acquire()
    global_jobs[key] = value
    global_job_lock.release()
    return value

def get_job(key):
    try:
        global_job_lock.acquire()
        global_jobs[key]
    except KeyError:
        global_jobs[key] = None
    finally:
        global_job_lock.release()
        return global_jobs[key]

def del_job(key):
    try:
        global_job_lock.acquire()
        del global_jobs[key]
    except KeyError:
        pass
    finally:
        global_job_lock.release()

def worker():
    running_jobs_count = 0
    
    global_job_lock.acquire()
    
    for key in global_jobs.keys():
        if global_jobs[key]["process"] != None:
            if global_jobs[key]["process"].is_alive():
                running_jobs_count += 1
            else:
                del global_jobs[key]
        
    for key in global_jobs.keys():
        if running_jobs_count < MAX_JOBS:
            if global_jobs[key]["process"] == None:
                global_jobs[key]["process"] = Thread(target = run_procedure, \
                                                     args = (global_jobs[key]["hstuuid"], \
                                                             global_jobs[key]["prcuuid"], \
                                                             global_jobs[key]["session"]))
                global_jobs[key]["start time"] = time()
                global_jobs[key]["process"].start()
                running_jobs_count += 1
        
    global_job_lock.release()
    
    sleep(1)
    
    Thread(target = worker).start()

def queue_procedure(hstuuid, prcuuid, session):
    add_message("Queued host: {0}, procedure {1}...".format(hstuuid, prcuuid))
    
    job = {
        "hstuuid" : hstuuid,
        "prcuuid" : prcuuid,
        "session" : session,
        "process" : None,
        "queue time" : time(),
        "start time" : None,
    }
    
    set_job(sucky_uuid(), job)

class TaskError:
    def __init__(self, uuid):
        self.output = ['<font color="red">'] + traceback.format_exc().split("\n") + ["</font>"]
        self.uuid = uuid
        self.status = 5 

    def execute(self, cli):
        return self.status
    
def run_procedure(hstuuid, prcuuid, session):
    add_message("Executing host: {0}, procedure {1}...".format(hstuuid, prcuuid))
    
    inventory = Collection("inventory")
    results = RAMCollection("results")
    
    result = results.get_object()
    
    result.object['start'] = time()
    result.object["output"] = []
    
    status_code_body = ""
    status_data = {}
    
    result.object["output"].append("importing status codes...")
    for status in inventory.find(type = "status"):
        try:
            status_code_body += "{0}=int('{1}')\n".format(status.object["alias"], status.object["code"])
            status_data[int(status.object["code"])] = status.object
        except Exception:
            result.object["output"] += traceback.format_exc().split("\n")
    
    host = inventory.get_object(hstuuid)
    result.object['host'] = host.object
    result.object['procedure'] = inventory.get_object(prcuuid).object
        
    tempmodule = new_module("tempmodule")
    
    winning_status = None
    continue_procedure = True
    
    result.object["tasks"] = []
    
    result.object['rfcs'] = []
    for rfcuuid in inventory.get_object(prcuuid).object["rfcs"]:
        result.object['rfcs'].append(inventory.get_object(rfcuuid).object)
    
    try:
        try:
            result.object["output"].append("importing console...")
            exec inventory.get_object(host.object["console"]).object["body"] in tempmodule.__dict__
            cli = tempmodule.Console(session = session, host = host.object["host"])
        except Exception:
            result.object["output"] += traceback.format_exc().split("\n")
        
        for tskuuid in inventory.get_object(prcuuid).object["tasks"]:
            task_result = inventory.get_object(tskuuid).object
            
            try:
                result.object["output"].append("importing task {0}...".format(inventory.get_object(tskuuid).object["name"]))
                exec status_code_body + inventory.get_object(tskuuid).object["body"] in tempmodule.__dict__
                task = tempmodule.Task()
                
                if continue_procedure:
                    task_result["start"] = time()
                    
                    try:
                        task.execute(cli)
                    except Exception:
                        task = TaskError(tskuuid)
                    
                    task_result["stop"] = time()
            except Exception:
                task = TaskError(tskuuid)
                result.object["output"] += traceback.format_exc().split("\n")
            
            task_result["output"] = task.output
            try:
                task_result["status"] = status_data[task.status]
                try:
                    if not inventory.get_object(prcuuid).object["continue {0}".format(task.status)]:
                        continue_procedure = False
                except Exception:
                    continue_procedure = False
            except Exception:
                task_result['status'] = {"code" : task.status}
                continue_procedure = False
                
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

    result.set()
    touch_flag("results")
    
    return result.object

Thread(target = worker).start()