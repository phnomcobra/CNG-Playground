#!/usr/bin/python
################################################################################
# TASK
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/08/2016 Original construction
################################################################################

import cherrypy
import json

from ..model.inventory import get, set

class Task(object):
    @cherrypy.expose
    def post_body(self):
        cl = cherrypy.request.headers['Content-Length']
        json_object = json.loads(cherrypy.request.body.read(int(cl)))
        set(json_object["id"], body = json_object["body"])
    
    @cherrypy.expose
    def get_body(self, id):
        return get(id, body = "body")["body"]
    
    @cherrypy.expose
    def get_ace_session(self):
        id = "ASdfasdf"
        #return json.dumps({"resp" : edit_python_view(id), "item" : id})
        return json.dumps({})
    