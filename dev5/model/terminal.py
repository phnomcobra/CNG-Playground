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
cli_sessions = {}

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

def write_file(sessionID, hstuuid, file):
    try:
        cli_sessions[sessionID + '-' + hstuuid].putf(file)
    except Exception:
        add_message(traceback.format_exc())
        
def create_session(sessionID, hstuuid, session):
    try:
        cli_id = sessionID + '-' + hstuuid
    
        inventory = Collection("inventory")
        host = inventory.get_object(hstuuid)
        tempmodule = new_module("tempmodule")
        exec inventory.get_object(host.object["console"]).object["body"] in tempmodule.__dict__
        
        if "send" not in dir(tempmodule.Console):
            raise Exception, "send method not present in console object!"
        
        if "recv" not in dir(tempmodule.Console):
            raise Exception, "recv method not present in console object!"
        
        cli_sessions[cli_id] = tempmodule.Console(session = session, host = host.object["host"])
    except Exception:
        cli_sessions[cli_id] = ErrorConsole(traceback.format_exc())
        add_message(traceback.format_exc())

def destroy_session(sessionID, hstuuid):
    cli_id = sessionID + '-' + hstuuid
    
    try:
        try:
            cli_sessions[cli_id].close()
        except Exception:
            add_message(traceback.format_exc())
        finally:
            del cli_sessions[cli_id]
    except Exception:
        add_message(traceback.format_exc())