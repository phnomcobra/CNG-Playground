#!/usr/bin/python
################################################################################
# TERMINAL
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 01/09/2017 Original construction
################################################################################

import traceback

from threading import Lock
from imp import new_module

from ..controller.messaging import add_message

from .document import Collection

global cli_sessions
global cli_sessions_lock
cli_sessions = {}
cli_sessions_lock = Lock()

class ErrorConsole:
    def __init__(self, message):
        self.__buffer = message
    
    def send(self, input_buffer):
        pass
    
    def recv(self):
        output_buffer = self.__buffer
        self.__buffer = ''
        return output_buffer

def send(sessionID, hstuuid, buffer):
    try:
        cli_sessions[sessionID + '-' + hstuuid].send(buffer)
    except Exception:
        add_message(traceback.format_exc())

def recv(sessionID, hstuuid):
    try:
        return cli_sessions[sessionID + '-' + hstuuid].recv()
    except Exception:
        add_message(traceback.format_exc())
        return traceback.format_exc()
    
def create_session(sessionID, hstuuid, session):
    inventory = Collection("inventory")
    
    cli_id = sessionID + '-' + hstuuid
    
    tempmodule = new_module("tempmodule")
    
    host = inventory.get_object(hstuuid)
    
    try:
        cli_sessions_lock.acquire()
        cli_sessions[cli_id] = ErrorConsole("Connecting to {0}...".format(host.object["host"]))
        
        exec inventory.get_object(host.object["console"]).object["body"] in tempmodule.__dict__
        
        if "send" not in dir(tempmodule.Console):
            raise Exception, "send method not present in console object!"
        
        if "recv" not in dir(tempmodule.Console):
            raise Exception, "recv method not present in console object!"
        
        cli_sessions[cli_id] = tempmodule.Console(session = session, host = host.object["host"])
    except Exception:
        cli_sessions[cli_id] = ErrorConsole(traceback.format_exc())
        add_message(traceback.format_exc())
    finally:
        cli_sessions_lock.release()

def destroy_session(sessionID, hstuuid):
    cli_id = sessionID + '-' + hstuuid
    
    try:
        cli_sessions_lock.acquire()
        cli_sessions[cli_id].close()
    except Exception:
        add_message(traceback.format_exc())
    finally:
        del cli_sessions[cli_id]
        cli_sessions_lock.release()