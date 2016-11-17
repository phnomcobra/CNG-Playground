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

from ..model.document import Collection
from ..model.inventory import get_child_nodes, \
                              set_parent_objuuid, \
                              get_context_menu, \
                              delete_node, \
                              create_container, \
                              create_task, \
                              create_procedure, \
                              create_controller, \
                              create_rfc

class Inventory(object):
    @cherrypy.expose
    def ajax_roots(self, objuuid):
        return json.dumps(get_child_nodes(objuuid))
    
    @cherrypy.expose
    def ajax_move(self, objuuid, parent_objuuid):
        set_parent_objuuid(objuuid, parent_objuuid)
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_create_container(self, objuuid):
        create_container(objuuid, "New Container")
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_create_task(self, objuuid):
        create_task(objuuid, "New Task")
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_create_procedure(self, objuuid):
        create_procedure(objuuid, "New Procedure")
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_create_controller(self, objuuid):
        create_controller(objuuid, "New Controller")
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_create_rfc(self, objuuid):
        create_rfc(objuuid, "New RFC")
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_delete(self, objuuid):
        delete_node(objuuid)
        return json.dumps({})
    
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
    def ajax_post_object(self):
        cl = cherrypy.request.headers['Content-Length']
        object = json.loads(cherrypy.request.body.read(int(cl)))
        
        collection = Collection("inventory")
        current = collection.get_object(object["objuuid"])
        current.object = object
        current.set()
        
        return json.dumps(current.object)