#!/usr/bin/python
################################################################################
# AUTH
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 12/30/2016 Original construction
################################################################################

import traceback

from .document import Collection
from .utils import sucky_uuid

def create_user(name = "New User", objuuid = None):
    collection = Collection("users")
    user = collection.get_object(objuuid)
    user.object = {
        "name" : name,
        "first name" : "",
        "last name" : "",
        "phone" : "",
        "email" : "",
        "organization" : "",
        "password" : "",
        "enabled" : True,
        "role" : "",
        "session" : {},
        
    }
    user.set()
    return user

def get_users_grid():
    collection = Collection("users")
    
    grid_data = []
    
    for usruuid in collection.list_objuuids():
        user = collection.get_object(usruuid)
        grid_data.append({"name" : user.object["name"], "objuuid" : user.object["objuuid"]})
        
    return grid_data

collection = Collection("users")
collection.create_attribute("group", "['group']")
collection.create_attribute("name", "['name']")
collection.create_attribute("enabled", "['enabled']")

if len(collection.find(name = "root")) == 0:
    user = create_user("root")
    user.object["role"] = "admin"
    user.object["password"] = "root"
    user.set()