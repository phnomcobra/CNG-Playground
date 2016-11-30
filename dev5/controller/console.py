#!/usr/bin/python
################################################################################
# HOST
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/28/2016 Original construction
################################################################################

import cherrypy
import json

from ..model.console import get_consoles

class Console(object):
    @cherrypy.expose
    def ajax_get_consoles(self):
        return json.dumps(get_consoles())