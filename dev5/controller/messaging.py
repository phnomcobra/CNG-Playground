#!/usr/bin/python
################################################################################
# MESSAGING
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/16/2016 Original construction
################################################################################

import cherrypy
import json

from time import time
from random import randrange

class Messaging(object):
    def __init__(self):
        self.messages = {"messages":[]}
    
    @cherrypy.expose
    def ajax_add_message(self, message, timestamp):
        self.add_message(message, timestamp)
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_add_message(self, message):
        self.add_message(message, time())
        return json.dumps({})
    
    def add_message(self, message, timestamp):
        self.messages["messages"] = [{"message" : message, "timestamp" : timestamp}] + \
                                    self.messages["messages"][:4]
    
    def get_messages(self):
        return self.messages
    
    @cherrypy.expose
    def ajax_get_messages(self):
        return json.dumps(self.get_messages())