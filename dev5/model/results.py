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

RAMCollection("results").destroy()
    
collection = RAMCollection("results")
collection.create_attribute("start", "['start']")
collection.create_attribute("stop", "['stop']")
collection.create_attribute("tskuuid", "['task']['objuuid']")
collection.create_attribute("prcuuid", "['procedure']['objuuid']")
collection.create_attribute("hstuuid", "['host']['objuuid']")