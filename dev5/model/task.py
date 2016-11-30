#!/usr/bin/python
################################################################################
# TASK
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/30/2016 Original construction
################################################################################

import traceback

from .document import Collection

from imp import new_module

def get_host_grid(tskuuid):
    collection = Collection("inventory")
    
    task = collection.get_object(tskuuid)
    
    grid_data = []
    
    for hstuuid in task.object["hosts"]:
        host = collection.get_object(hstuuid)
        
        grid_data.append({"name" : host.object["name"], "host" : host.object["host"], "objuuid" : host.object["objuuid"]})
        
    return grid_data

def execute(tskuuid, hstuuid, session):
    collection = Collection("inventory")
    
    for status in collection.find(type = "status"):
        try:
            print "exec: {0}=int('{1}')".format(status.object["alias"], status.object["code"])
            exec("{0}=int('{1}')".format(status.object["alias"], status.object["code"]))
        except Exception:
            print "Exception:", traceback.format_exc()
    
    host = collection.get_object(hstuuid)
    
    try:
        print "imp: Load CLI"
        tempmodule = new_module("tempmodule")
        exec collection.get_object(host.object["console"]).object["body"] in tempmodule.__dict__
        cli = tempmodule.Console(session = session, host = host.object["host"])
        
        for line in dir(cli):
            print "imp:", line
    except Exception:
        print "Exception:", traceback.format_exc()
    
    try:
        print "imp: Load Task"
        tempmodule = new_module("tempmodule")
        exec collection.get_object(tskuuid).object["body"] in tempmodule.__dict__
        task = tempmodule.Task()
        
        for line in dir(task):
            print "task:", line
    except Exception:
        print "Exception:", traceback.format_exc()
    
    
    return {}