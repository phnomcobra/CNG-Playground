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

def update_job(jobuuid, key, value):
    global_job_lock.acquire()
    global_jobs[jobuuid][key] = value
    global_job_lock.release()
    touch_flag("queueState")
    
def set_job(jobuuid, value):
    global_job_lock.acquire()
    global_jobs[jobuuid] = value
    global_job_lock.release()
    touch_flag("queueState")

def get_job(jobuuid):
    try:
        global_job_lock.acquire()
        global_jobs[jobuuid]
    except KeyError:
        global_jobs[jobuuid] = None
    finally:
        global_job_lock.release()
        return global_jobs[jobuuid]

def del_job(jobuuid):
    try:
        global_job_lock.acquire()
        del global_jobs[jobuuid]
    except KeyError:
        pass
    finally:
        touch_flag("queueState")
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
                touch_flag("queueState")
        
    for key in global_jobs.keys():
        if running_jobs_count < MAX_JOBS:
            if global_jobs[key]["process"] == None:
                global_jobs[key]["process"] = Thread(target = run_procedure, \
                                                     args = (global_jobs[key]["host"]["objuuid"], \
                                                             global_jobs[key]["procedure"]["objuuid"], \
                                                             global_jobs[key]["session"], \
                                                             global_jobs[key]["jobuuid"]))
                global_jobs[key]["start time"] = time()
                global_jobs[key]["process"].start()
                running_jobs_count += 1
                touch_flag("queueState")
        
    global_job_lock.release()
    
    sleep(1)
    
    Thread(target = worker).start()

def get_jobs_grid():
    grid_data = {}
    global_job_lock.acquire()
    
    for jobuuid, dict in global_jobs.iteritems():
        if dict["start time"]:
            grid_data[jobuuid] = {}
            grid_data[jobuuid]["name"] = dict["procedure"]["name"]
            grid_data[jobuuid]["host"] = dict["host"]["name"]
            grid_data[jobuuid]["progress"] = dict["progress"]
            grid_data[jobuuid]["message"] = dict["message"]
            grid_data[jobuuid]["start time"] = dict["start time"]
    
    global_job_lock.release()
    
    return grid_data

def queue_procedure(hstuuid, prcuuid, session):
    add_message("Queued host: {0}, procedure {1}...".format(hstuuid, prcuuid))
    
    inventory = Collection("inventory")
    
    jobuuid = sucky_uuid()
    
    job = {
        "jobuuid" : jobuuid,
        "host" : inventory.get_object(hstuuid).object,
        "procedure" : inventory.get_object(prcuuid).object,
        "session" : session,
        "process" : None,
        "queue time" : time(),
        "start time" : None,
        "progress" : 0,
        "message" : "Queued",
    }
    
    set_job(jobuuid, job)

class TaskError:
    def __init__(self, uuid):
        self.output = ['<font color="red">'] + traceback.format_exc().split("\n") + ["</font>"]
        self.uuid = uuid
        self.status = 5 

    def execute(self, cli):
        return self.status
    
def run_procedure(hstuuid, prcuuid, session, jobuuid = None):
    add_message("Executing host: {0}, procedure {1}...".format(hstuuid, prcuuid))
    
    if jobuuid:
        update_job(jobuuid, "message", "Executing")
    
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
        
        tskuuids = inventory.get_object(prcuuid).object["tasks"]
        for seq_num, tskuuid in enumerate(tskuuids):
            task_result = inventory.get_object(tskuuid).object
            
            try:
                result.object["output"].append("importing task {0}...".format(inventory.get_object(tskuuid).object["name"]))
                
                if jobuuid:
                    update_job(jobuuid, "message", "Executing Task: " + inventory.get_object(tskuuid).object["name"])
                
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
            
            if jobuuid:
                update_job(jobuuid, "progress", float(seq_num + 1) / float(len(tskuuids)))
    except Exception:
        add_message(traceback.format_exc())
        
    result.object['stop'] = time()

    result.set()
    touch_flag("results")
    
    return result.object

Thread(target = worker).start()