#!/usr/bin/python
################################################################################
# TASK
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/30/2016 Original construction
################################################################################

import cherrypy
import json

from ..model.task import get_host_grid, execute

class Task(object):
    @cherrypy.expose
    def ajax_get_host_grid(self, objuuid):
        return json.dumps(get_host_grid(objuuid))
    
    @cherrypy.expose
    def ajax_execute_task(self, tskuuid, hstuuid):
        return json.dumps(execute(tskuuid, hstuuid, cherrypy.session))