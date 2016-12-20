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
import traceback

from .messaging import add_message

from ..model.procedure import get_task_grid, \
                              get_host_grid, \
                              queue_procedure, \
                              run_procedure

class Procedure(object):
    @cherrypy.expose
    def ajax_get_task_grid(self, objuuid):
        add_message("procedure controller: get procedure task grid: {0}".format(objuuid))
        try:
            return json.dumps(get_task_grid(objuuid))
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_get_host_grid(self, objuuid):
        add_message("procedure controller: get procedure host grid: {0}".format(objuuid))
        try:
            return json.dumps(get_host_grid(objuuid))
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_execute_procedure(self, prcuuid, hstuuid):
        add_message("procedure controller: execute procedure: hstuuid: {0}, prcuuid: {1}".format(hstuuid, prcuuid))
        try:
            session = {}
            for key, value in cherrypy.session.items():
                session[key] = value
            return json.dumps(run_procedure(hstuuid, prcuuid, session))
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_queue_procedure(self, prcuuid, hstuuid):
        add_message("procedure controller: queuing procedure: hstuuid: {0}, prcuuid: {1}".format(hstuuid, prcuuid))
        try:
            session = {}
            for key, value in cherrypy.session.items():
                session[key] = value
            queue_procedure(hstuuid, prcuuid, session)
            return json.dumps({})
        except Exception:
            add_message(traceback.format_exc())