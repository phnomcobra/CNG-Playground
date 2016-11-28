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

from ..view.index import index_view
from .inventory import Inventory
from .messaging import Messaging
from .procedure import Procedure
from .controller import Controller
from .credentials import Credentials
from .rfc import RFC

class Root(object):
    inventory = Inventory()
    messaging = Messaging()
    procedure = Procedure()
    controller = Controller()
    credentials = Credentials()
    rfc = RFC()

    @cherrypy.expose
    def index(self):
        return index_view()