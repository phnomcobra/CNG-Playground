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

from ..model.procedure import get_task_grid

class Procedure(object):
    @cherrypy.expose
    def ajax_get_task_grid(self, objuuid):
        return json.dumps(get_task_grid(objuuid))