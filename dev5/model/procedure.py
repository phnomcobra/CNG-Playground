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

from .document import Collection
from .utils import sucky_uuid

def get_task_grid(prcuuid):
    collection = Collection("inventory")
    
    procedure = collection.get_object(prcuuid)
    
    grid_data = []
    
    for tskuuid in procedure.object["tasks"]:
        task = collection.get_object(tskuuid)
        
        grid_data.append({"name" : task.object["name"], "objuuid" : task.object["objuuid"]})
        
    return grid_data

def get_related_procedure_grid(prcuuid):
    collection = Collection("inventory")
    
    procedure = collection.get_object(prcuuid)
    
    grid_data = []
    
    for prcuuid in procedure.object["procedures"]:
        related_procedure = collection.get_object(prcuuid)
        
        grid_data.append({"name" : related_procedure.object["name"], "objuuid" : related_procedure.object["objuuid"]})
        
    return grid_data