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
    
    controller = Collection("inventory").get_object(ctruuid)
    
    controller_results = []
    
    for hstuuid in controller.object["hosts"]:
        for prcuuid in controller.object["procedures"]:
            try:
                controller_results.append(results.find(hstuuid = hstuuid, prcuuid = prcuuid)[0].object)
            except IndexError:
                pass
    
    return controller_results

def get_procedure_result(prcuuid, hstuuid):
    try:
        return RAMCollection("results").find(hstuuid = hstuuid, prcuuid = prcuuid)[0].object
    except IndexError:
        return None
    

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