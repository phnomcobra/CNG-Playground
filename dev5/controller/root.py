#!/usr/bin/python
################################################################################
# ROOT
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/16/2016 Original construction
################################################################################

import cherrypy
import json

from random import random
from ..view.index import index_view
from .inventory import Inventory
from .messaging import Messaging
from .task import Task
from .tabs import Tabs

class Root(object):
    inventory = Inventory()
    messaging = Messaging()
    task = Task()
    tabs = Tabs()

    @cherrypy.expose
    def index(self):
        return index_view()