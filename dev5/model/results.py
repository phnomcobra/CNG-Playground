#!/usr/bin/python
################################################################################
# RESULTS
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 12/05/2016 Original construction
################################################################################

import traceback

from threading import Thread
from time import time, sleep

from .document import Collection
from .ramdocument import Collection as RAMCollection
from .utils import sucky_uuid

def delete(objuuid):
    collection = RAMCollection("results")
    collection.get_object(objuuid).destroy()

def get_controller_results(ctruuid):
    results = RAMCollection("results")
    inventory = Collection("inventory")
    
    controller = inventory.get_object(ctruuid)
    
    controller_results = []
    
    for hstuuid in controller.object["hosts"]:
        for prcuuid in controller.object["procedures"]:
            stop_time = None
            
            controller_result = None
            
            for result in results.find(hstuuid = hstuuid, prcuuid = prcuuid):
                if result.object["stop"]:
                    if stop_time == None:
                        stop_time = int(result.object["stop"])
                        controller_result = result.object
                    elif int(result.object["stop"]) > stop_time:
                        stop_time = int(result.object["stop"])
                        controller_result = result.object
                elif stop_time == None:
                    controller_result = result.object
            
            if controller_result:
                controller_results.append(controller_result)
    
    return controller_results

def get_procedure_result(prcuuid, hstuuid):
    results = RAMCollection("results")
    
    stop_time = None
            
    procedure_result = None
            
    for result in results.find(hstuuid = hstuuid, prcuuid = prcuuid):
        if result.object["stop"]:
            if stop_time == None:
                stop_time = int(result.object["stop"])
                procedure_result = result.object
            elif int(result.object["stop"]) > stop_time:
                stop_time = int(result.object["stop"])
                procedure_result = result.object
        elif stop_time == None:
            procedure_result = result.object
    
    return procedure_result

def worker():
    results = RAMCollection("results")
    
    for objuuid in results.list_objuuids():
        result = results.get_object(objuuid)
        
        try:
            if time() - result.object["start"] > 28800:
                result.destroy()
        except Exception:
            result.destroy()
    
    sleep(3600)
    
    Thread(target = worker).start()

collection = RAMCollection("results")
collection.create_attribute("start", "['start']")
collection.create_attribute("stop", "['stop']")
collection.create_attribute("tskuuid", "['task']['objuuid']")
collection.create_attribute("prcuuid", "['procedure']['objuuid']")
collection.create_attribute("hstuuid", "['host']['objuuid']")

Thread(target = worker).start()