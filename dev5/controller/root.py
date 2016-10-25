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
from .inventory import Tree

class Root(object):
    tree = Tree()

    @cherrypy.expose
    def index(self):
        return index_view()

    @cherrypy.expose
    def get_dummy(self, item):
        print "dummy load:"
        return json.dumps({"resp":"blah {0}".format(random()), "item":item})
