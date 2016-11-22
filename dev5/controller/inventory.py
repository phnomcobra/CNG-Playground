#!/usr/bin/python
################################################################################
# INVENTORY
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/16/2016 Original construction
################################################################################

import cherrypy
import json

from time import sleep

from ..model.document import Collection
from ..model.inventory import get_child_nodes, \
                              get_status_objects, \
                              set_parent_objuuid, \
                              get_context_menu, \
                              delete_node, \
                              create_container, \
                              create_task, \
                              create_procedure, \
                              create_controller, \
                              create_rfc, \
                              create_status_code, \
                              create_host

class Inventory(object):
    def __init__(self):
        self.moving = False

    @cherrypy.expose
    def ajax_roots(self, objuuid):
        return json.dumps(get_child_nodes(objuuid))
    
    @cherrypy.expose
    def ajax_move(self, objuuid, parent_objuuid):
        while self.moving:
            sleep(.1)
        
        try:
            self.moving = True
            set_parent_objuuid(objuuid, parent_objuuid)
        except Exception as e:
            pass
        finally:
            self.moving = False
            
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_create_container(self, objuuid):
        return json.dumps(create_container(objuuid, "New Container"))
    
    @cherrypy.expose
    def ajax_create_host(self, objuuid):
        return json.dumps(create_host(objuuid, "New Host"))
    
    @cherrypy.expose
    def ajax_create_task(self, objuuid):
        return json.dumps(create_task(objuuid, "New Task"))
    
    @cherrypy.expose
    def ajax_create_status_code(self, objuuid):
        return json.dumps(create_status_code(objuuid, "New Status Code"))
    
    @cherrypy.expose
    def ajax_create_procedure(self, objuuid):
        return json.dumps(create_procedure(objuuid, "New Procedure"))
    
    @cherrypy.expose
    def ajax_create_controller(self, objuuid):
        return json.dumps(create_controller(objuuid, "New Controller"))
    
    @cherrypy.expose
    def ajax_create_rfc(self, objuuid):
        return json.dumps(create_rfc(objuuid, "New RFC"))
    
    @cherrypy.expose
    def ajax_delete(self, objuuid):
        while self.moving:
            sleep(.1)
            
        delete_node(objuuid)
        return json.dumps({"id" : objuuid})
    
    @cherrypy.expose
    def ajax_context(self, objuuid):
        return json.dumps(get_context_menu(objuuid))
    
    @cherrypy.expose
    def ajax_select(self, objuuid):
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_get_object(self, objuuid):
        collection = Collection("inventory")
        return json.dumps(collection.get_object(objuuid).object)
    
    @cherrypy.expose
    def ajax_get_status_objects(self):
        return json.dumps(get_status_objects())
    
    @cherrypy.expose
    def ajax_post_object(self):
        cl = cherrypy.request.headers['Content-Length']
        object = json.loads(cherrypy.request.body.read(int(cl)))
        
        collection = Collection("inventory")
        current = collection.get_object(object["objuuid"])
        current.object = object
        current.set()
        
        return json.dumps(current.object)