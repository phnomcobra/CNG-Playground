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
                              create_controller

class Inventory(object):
    @cherrypy.expose
    def ajax_roots(self, id):
        return json.dumps(get_child_nodes(id))
    
    @cherrypy.expose
    def ajax_move(self, id, parent):
        set_parent_objuuid(id, parent)
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_create_container(self, id):
        create_container(id, "New Container")
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_create_task(self, id):
        create_task(id, "New Task")
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_create_procedure(self, id):
        create_procedure(id, "New Procedure")
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_create_controller(self, id):
        create_controller(id, "New Controller")
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_delete(self, id):
        delete_node(id)
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_context(self, id):
        return json.dumps(get_context_menu(id))
    
    @cherrypy.expose
    def ajax_select(self, id):
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_get_object(self, id):
        collection = Collection("inventory")
        return json.dumps(collection.get_object(id).object)
    
    @cherrypy.expose
    def ajax_post_object(self):
        cl = cherrypy.request.headers['Content-Length']
        object = json.loads(cherrypy.request.body.read(int(cl)))
        
        collection = Collection("inventory")
        current = collection.get_object(object["objuuid"])
        current.object = object
        current.set()
        
        return json.dumps(current.object)