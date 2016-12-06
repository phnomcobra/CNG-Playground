#!/usr/bin/python
################################################################################
# CONTROLLER
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/23/2016 Original construction
################################################################################

import cherrypy
import json

from ..model.controller import get_procedure_grid, get_host_grid, get_tiles

class Controller(object):
    @cherrypy.expose
    def ajax_get_procedure_grid(self, objuuid):
        return json.dumps(get_procedure_grid(objuuid))
    
    @cherrypy.expose
    def ajax_get_host_grid(self, objuuid):
        return json.dumps(get_host_grid(objuuid))
        
    @cherrypy.expose
    def ajax_get_tiles(self, objuuid):
        return json.dumps(get_tiles(objuuid))