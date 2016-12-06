#!/usr/bin/python
################################################################################
# RESULTS
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 12/06/2016 Original construction
################################################################################

import cherrypy
import json

from ..model.results import get_controller_results

class Results(object):
    @cherrypy.expose
    def ajax_get_controller(self, objuuid):
        return json.dumps(get_controller_results(objuuid))