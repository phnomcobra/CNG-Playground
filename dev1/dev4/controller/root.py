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
from random import randrange

class Root(object):
    @cherrypy.expose
    def index(self):
        return index_view()

    @cherrypy.expose
    def ajax_roots(self, id):
        print id
        return json.dumps([
       { "id" : "ajson1{0}".format(randrange(0, 9, 1)), "parent" : "#", "text" : "Simple root node{0}".format(randrange(0, 9, 1)) },
       { "id" : "ajson2", "parent" : "#", "text" : "Root node 2" },
       { "id" : "ajson3", "parent" : "ajson2", "text" : "Child 1" },
       { "id" : "ajson4{0}".format(randrange(0, 9, 1)), "parent" : "ajson2", "text" : "Child 2{0}".format(randrange(0, 9, 1)) },
    ])
    
    @cherrypy.expose
    def ajax_create(self, id):
        print id
        return json.dumps({"text" : "success"})
    
    @cherrypy.expose
    def ajax_select(self, id):
        print id
        return json.dumps({"text" : "success"})