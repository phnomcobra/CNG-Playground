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

from cherrypy.lib.static import serve_fileobj

from .messaging import add_message
from ..model.terminal import create_session, \
                             destroy_session, \
                             write_file, \
                             send, \
                             recv

class Terminal(object):
    @cherrypy.expose
    def ajax_create_session(self, hstuuid):
        add_message("terminal controller: create terminal")
        try:
            session = {}
            for key, value in cherrypy.session.items():
                session[key] = value
        
            return json.dumps({"ttyuuid" : create_session(hstuuid, session)})
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_destroy_session(self, ttyuuid):
        add_message("terminal controller: destroy terminal: {0}".format(ttyuuid))
        try:
            destroy_session(ttyuuid)
            return json.dumps({})
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_send(self, ttyuuid, buffer):
        try:
            send(ttyuuid, buffer)
            return json.dumps({})
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def ajax_recv(self, ttyuuid):
        try:
            return recv(ttyuuid)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    def put_file(self, file, ttyuuid):
        add_message("terminal controller: upload file: {0}".format(file.filename))
        
        try:
            write_file(ttyuuid, file)
        except Exception:
            add_message(traceback.format_exc())
        
        return json.dumps({})