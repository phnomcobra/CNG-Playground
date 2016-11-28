#!/usr/bin/python
################################################################################
# CREDENTIALS
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/28/2016 Original construction
################################################################################

import cherrypy
import json

class Credentials(object):
    @cherrypy.expose
    def ajax_set(self, credentials):
        return json.dumps(credentials)
