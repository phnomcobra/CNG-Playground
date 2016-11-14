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

from ..view.procedure import edit_view, \
                             attribute_view

class Procedure(object):
    @cherrypy.expose
    def edit(self, description):
        return edit_view(description)
    
    @cherrypy.expose
    def attributes(self, name, title, objuuid):
        return attribute_view(name, title, objuuid)