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

from ..model.inventory import get_child_nodes, \
                              set_parent_objuuid, \
                              get_context_menu, \
                              delete_node, \
                              create_container

class Inventory(object):
    def __init__(self):
        self.tabs = {}
    
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
    def ajax_delete(self, id):
        delete_node(id)
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_context(self, id):
        return json.dumps(get_context_menu(id))
    
    @cherrypy.expose
    def ajax_get_tabs(self):
        return json.dumps(self.tabs)
    
    @cherrypy.expose
    def ajax_close_tab(self, item):
        del self.tabs[item];
        return json.dumps({})
    
    @cherrypy.expose
    def ajax_select(self, id):
        return json.dumps({})