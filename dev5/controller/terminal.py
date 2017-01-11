#!/usr/bin/python
################################################################################
# TERMINAL
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 01/09/2017 Original construction
################################################################################

import cherrypy
import json
import traceback

from .messaging import add_message

from ..model.terminal import create_session, \
                             destroy_session, \
                             send, \
                             recv

class Terminal(object):
    @cherrypy.expose
    def ajax_create_session(self, hstuuid):
        add_message("terminal controller: create session: {0}".format(hstuuid))
        try:
            session = {}
            for key, value in cherrypy.session.items():
                session[key] = value
        
            create_session(cherrypy.session.id, hstuuid, session)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_destroy_session(self, hstuuid):
        add_message("terminal controller: destroy session: {0}".format(hstuuid))
        try:
            destroy_session(cherrypy.session.id, hstuuid)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_send(self, hstuuid, buffer):
        try:
            send(cherrypy.session.id, hstuuid, buffer)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_recv(self, hstuuid):
        try:
            return recv(cherrypy.session.id, hstuuid)
        except Exception:
            add_message(traceback.format_exc())