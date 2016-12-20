#!/usr/bin/python
################################################################################
# CONTROLLER
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/23/2016 Original construction
################################################################################

from threading import Thread

from .document import Collection
from .utils import sucky_uuid

def get_procedure_grid(ctruuid):
    collection = Collection("inventory")
    
    controller = collection.get_object(ctruuid)
    
    grid_data = []
    
    for prcuuid in controller.object["procedures"]:
        procedure = collection.get_object(prcuuid)
        
        if "type" in procedure.object:
            grid_data.append({"name" : procedure.object["name"], "objuuid" : procedure.object["objuuid"]})
        else:
            add_message("procedure {0} is missing!".format(prcuuid))
            grid_data.append({"name" : "MISSING!", "objuuid" : prcuuid})
        
    return grid_data

def get_host_grid(ctruuid):
    collection = Collection("inventory")
    
    controller = collection.get_object(ctruuid)
    
    grid_data = []
    
    for hstuuid in controller.object["hosts"]:
        host = collection.get_object(hstuuid)
        
        if "type" in host.object:
            grid_data.append({"name" : host.object["name"], "host" : host.object["host"], "objuuid" : host.object["objuuid"]})
        else:
            add_message("host {0} is missing!".format(hstuuid))
            grid_data.append({"name" : "MISSING!", "host" : "?.?.?.?", "objuuid" : hstuuid})
        
    return grid_data

def get_tiles(ctruuid):
    collection = Collection("inventory")
    
    controller = collection.get_object(ctruuid)
    
    procedures = []
    for prcuuid in controller.object["procedures"]:
        procedures.append(collection.get_object(prcuuid).object)
    
    hosts = []
    for hstuuid in controller.object["hosts"]:
        host = collection.get_object(hstuuid)
        hosts.append(collection.get_object(hstuuid).object)
    
    return {"hosts" : hosts, "procedures" : procedures}