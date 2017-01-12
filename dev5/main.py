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
    
    config = {
        'log.screen': False,
        'tools.staticdir.on' : True,
        'tools.sessions.on' : True,
        'tools.sessions.locking' : 'explicit',
        'tools.auth.on' : True,
        'tools.staticdir.dir' : os.path.join(current_dir, './static'),
        'server.thread_pool' : 100,
        'server.socket_host' : '0.0.0.0',
        'server.socket_port' : 443,
        'server.ssl_module' : 'builtin',
        'server.ssl_certificate' : os.path.join(current_dir, './cert.pem'),
        'server.ssl_private_key' : os.path.join(current_dir, './privkey.pem')
        #'log.error_file': 'error.log'
    }
    
    cherrypy.config.update(config)
    
    cherrypy.quickstart(Root())
