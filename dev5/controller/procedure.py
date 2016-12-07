#!/usr/bin/python
################################################################################
# PROCEDURE
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/16/2016 Original construction
################################################################################

import cherrypy
import json

from ..model.procedure import get_task_grid, \
                              get_related_procedure_grid, \
                              get_related_procedures, \
                              get_host_grid, \
                              execute

class Procedure(object):
    @cherrypy.expose
    def ajax_get_task_grid(self, objuuid):
        return json.dumps(get_task_grid(objuuid))
    
    @cherrypy.expose
    def ajax_get_host_grid(self, objuuid):
        return json.dumps(get_host_grid(objuuid))
    
    @cherrypy.expose
    def ajax_get_related_procedure_grid(self, objuuid):
        return json.dumps(get_related_procedure_grid(objuuid))
    
    @cherrypy.expose
    def ajax_get_related_procedures(self, objuuid):
        return json.dumps(get_related_procedures(objuuid))
    
    @cherrypy.expose
    def ajax_execute_procedure(self, prcuuid, hstuuid):
        return json.dumps(execute(prcuuid, hstuuid, cherrypy.session))