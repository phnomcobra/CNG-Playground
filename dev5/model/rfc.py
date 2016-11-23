#!/usr/bin/python
################################################################################
# RFC
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/23/2016 Original construction
################################################################################

from .document import Collection
from .utils import sucky_uuid

def get_rfc_grid(prcuuid):
    collection = Collection("inventory")
    
    procedure = collection.get_object(prcuuid)
    
    grid_data = []
    
    for rfcuuid in procedure.object["rfcs"]:
        rfc = collection.get_object(rfcuuid)
        
        grid_data.append({"name" : rfc.object["name"], \
                          "number" : rfc.object["number"], \
                          "title" : rfc.object["title"], \
                          "objuuid" : rfc.object["objuuid"]})
    return grid_data