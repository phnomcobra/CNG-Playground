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
import traceback

from ..model.results import get_controller_results
from .messaging import add_message

class Results(object):
    @cherrypy.expose
    def ajax_get_controller(self, objuuid):
        add_message("results controller: get controller results: {0}".format(objuuid))
        try:
            return json.dumps(get_controller_results(objuuid))
        except Exception:
            add_message(traceback.format_exc())