#!/usr/bin/python
################################################################################
# RESULTS
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 12/05/2016 Original construction
# 06/05/2017 Replaced sleep with timer object
################################################################################

import traceback

from threading import Thread, Timer
from time import time

from .ramdocument import Collection as RAMCollection
from .document import Collection
from .utils import sucky_uuid

def delete(objuuid):
    collection = RAMCollection("results")
    collection.get_object(objuuid).destroy()

def get_controller_results(ctruuid):
    results = RAMCollection("results")
    
    collection = Collection("inventory")
    
    controller = collection.get_object(ctruuid)
    
    controller_results = []
    
    hstuuids = []
    for hstuuid in controller.object["hosts"]:
        o = collection.get_object(hstuuid)
        
        if o.object["type"] == "host":
            if hstuuid not in hstuuids:
                hstuuids.append(hstuuid)
        elif o.object["type"] == "host group":
            for uuid in o.object["hosts"]:
                if uuid not in hstuuids:
                    hstuuids.append(uuid)
    
    for hstuuid in hstuuids:
        for prcuuid in controller.object["procedures"]:
            try:
                controller_results.append(results.find(hstuuid = hstuuid, prcuuid = prcuuid)[0].object)
            except IndexError:
                pass
    
    return controller_results

def get_procedure_result(prcuuid, hstuuid):
    collection = Collection("inventory")
    
    results = RAMCollection("results")
    
    result_objects = []
    
    host = collection.get_object(hstuuid)
        
    hstuuids = []
    if host.object["type"] == "host":
        if hstuuid not in hstuuids:
            hstuuids.append(hstuuid)
    elif host.object["type"] == "host group":
        for hstuuid in host.object["hosts"]:
            if hstuuid not in hstuuids:
                hstuuids.append(hstuuid)

    for hstuuid in hstuuids:
        try:
            result_objects.append(results.find(hstuuid = hstuuid, prcuuid = prcuuid)[0].object)
        except IndexError:
            pass
    
    return result_objects
    

def worker():
    Timer(3600, worker).start()
    
    results = RAMCollection("results")
    
    for objuuid in results.list_objuuids():
        result = results.get_object(objuuid)
        
        try:
            if time() - result.object["start"] > 28800:
                result.destroy()
        except Exception:
            result.destroy()
    
collection = RAMCollection("results")
collection.create_attribute("start", "['start']")
collection.create_attribute("stop", "['stop']")
collection.create_attribute("tskuuid", "['task']['objuuid']")
collection.create_attribute("prcuuid", "['procedure']['objuuid']")
collection.create_attribute("hstuuid", "['host']['objuuid']")

Thread(target = worker).start()