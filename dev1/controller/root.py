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

from ..view.index import index_view
from random import random

class Root(object):
    @cherrypy.expose
    def index(self):
        return index_view()

    @cherrypy.expose
    def getrandom(self):
        return str(random())