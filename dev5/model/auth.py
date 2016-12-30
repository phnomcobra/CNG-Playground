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
        "pwhash" : "",
        "enabled" : True,
        "role" : ""
    }
    user.set()
    return user

collection = Collection("users")
collection.create_attribute("group", "['group']")
collection.create_attribute("name", "['name']")
collection.create_attribute("enabled", "['enabled']")
