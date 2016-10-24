#!/usr/bin/python
################################################################################
# ROOT
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/16/2016 Original construction
################################################################################

import cherrypy
import json

from ..view.index import index_view

class Root(object):
    def __init__(self):
        self.__text = ''
    
    @cherrypy.expose
    def index(self):
        return index_view()

    @cherrypy.expose
    def textarea(self):
        cl = cherrypy.request.headers['Content-Length']
        self.__text = cherrypy.request.body.read(int(cl))
    
    @cherrypy.expose
    def gettextarea(self):
       return self.__text