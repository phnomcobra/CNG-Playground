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
from .utils import sucky_uuid

def delete(objuuid):
    collection = Collection("results")
    collection.get_object(objuuid).destroy()

def create_task(parent_objuuid, name):
    collection = Collection("results")
    task = collection.get_object()
    task.object = {
        "type" : "task",
        "name" : name,
        "body" : "",
        "icon" : "/images/task_icon.png",
        "hosts" : [],
    }
    task.set()
    return task.object

collection = Collection("results")
collection.create_attribute("parent", "['parent']")
collection.create_attribute("type", "['type']")
collection.create_attribute("name", "['name']")
