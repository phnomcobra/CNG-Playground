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

from .document import Collection
from .utils import sucky_uuid
from ..controller.flags import touch_flag

def get_procedure_grid(ctruuid):
    collection = Collection("inventory")
    
    controller = collection.get_object(ctruuid)
    
    grid_data = []
    
    for prcuuid in controller.object["procedures"]:
        procedure = collection.get_object(prcuuid)
        
        grid_data.append({"name" : procedure.object["name"], "objuuid" : procedure.object["objuuid"]})
        
    return grid_data

def get_host_grid(ctruuid):
    collection = Collection("inventory")
    
    controller = collection.get_object(ctruuid)
    
    grid_data = []
    
    for hstuuid in controller.object["hosts"]:
        host = collection.get_object(hstuuid)
        
        grid_data.append({"name" : host.object["name"], "host" : host.object["host"], "objuuid" : host.object["objuuid"]})
        
    return grid_data

def get_tiles(ctruuid):
    collection = Collection("inventory")
    
    controller = collection.get_object(ctruuid)
    
    tiles = []
    hosts = []
    procedures = []
    
    for prcuuid in controller.object["procedures"]:
        procedures.append(collection.get_object(prcuuid).object)
    
    for x, hstuuid in enumerate(controller.object["hosts"]):
        host = collection.get_object(hstuuid)
        hosts.append(host.object)
        
        for y, prcuuid in enumerate(controller.object["procedures"]):
            procedure = collection.get_object(prcuuid)
            
            tile = {}
            tile["position"] = [x, y]
            tile["host"] = host.object
            tile["procedure"] = procedure.object
            tile["selected"] = False
            
            tile["procedures"] = []
            for rlpuuid in procedure.object["procedures"]:
                tile["procedures"].append(collection.get_object(rlpuuid).object)
            
            tiles.append(tile)
    
    return {"tiles" : tiles, "hosts" : hosts, "procedures" : procedures}