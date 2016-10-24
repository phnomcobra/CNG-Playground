#!/usr/bin/python
################################################################################
# MAIN
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/16/2016 Original construction
# 10/19/2016 Created start function
################################################################################

import cherrypy
import os

from .controller.root import Root

def start():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cherrypy.config.update({'environment': 'production',
                            'tools.staticdir.on': True,
                            'tools.staticdir.dir': os.path.join(current_dir, './static'),
                            'server.socket_host': '127.0.0.1'})

    cherrypy.quickstart(Root())
