#!/usr/bin/python
################################################################################
# MAIN
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/16/2016 Original construction
################################################################################

import cherrypy
import os

from dev1.controller.root import Root

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cherrypy.config.update({'environment': 'production',
                            'tools.staticdir.on': True,
                            'tools.staticdir.dir': os.path.join(current_dir, 'dev1/static'),
                            'server.socket_host': '0.0.0.0'})

    cherrypy.quickstart(Root())
