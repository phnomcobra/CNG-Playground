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
import traceback

from cherrypy.lib.static import serve_fileobj
from time import sleep, time

from .messaging import add_message

from .auth import require
from ..model.document import Collection
from ..model.inventory import get_child_nodes, \
                              get_status_objects, \
                              set_parent_objuuid, \
                              get_context_menu, \
                              delete_node, \
                              create_container, \
                              create_task, \
                              create_link, \
                              create_procedure, \
                              create_controller, \
                              create_rfc, \
                              create_status_code, \
                              create_host, \
                              create_console, \
                              get_dependencies, \
                              copy_object

class Inventory(object):
    def __init__(self):
        self.moving = False

    @cherrypy.expose
    @require()
    def ajax_roots(self, objuuid):
        add_message("inventory controller: load inventory: {0}".format(objuuid))
        try:
            return json.dumps(get_child_nodes(objuuid))
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_move(self, objuuid, parent_objuuid):
        add_message("inventory controller: move inventory object: {0}".format(objuuid))
        while self.moving:
            sleep(.1)
        
        try:
            self.moving = True
            set_parent_objuuid(objuuid, parent_objuuid)
        except Exception as e:
            add_message(traceback.format_exc())
        finally:
            self.moving = False
            
        return json.dumps({})
    
    @cherrypy.expose
    @require()
    def ajax_copy_object(self, objuuid):
        add_message("inventory controller: copy: {0}".format(objuuid))

        try:
            while self.moving:
                sleep(.1)
            
            return json.dumps(copy_object(objuuid).object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_create_container(self, objuuid):
        add_message("inventory controller: create container: {0}".format(objuuid))
        try:
            return json.dumps(create_container(objuuid, "New Container").object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_create_host(self, objuuid):
        add_message("inventory controller: create host: {0}".format(objuuid))
        try:
            return json.dumps(create_host(objuuid, "New Host").object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_create_console(self, objuuid):
        add_message("inventory controller: create console: {0}".format(objuuid))
        try:
            return json.dumps(create_console(objuuid, "New Console").object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_create_task(self, objuuid):
        add_message("inventory controller: create task: {0}".format(objuuid))
        try:
            return json.dumps(create_task(objuuid, "New Task").object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_create_status_code(self, objuuid):
        add_message("inventory controller: create status code: {0}".format(objuuid))
        try:
            return json.dumps(create_status_code(objuuid, "New Status Code").object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_create_procedure(self, objuuid):
        add_message("inventory controller: create procedure: {0}".format(objuuid))
        try:
            return json.dumps(create_procedure(objuuid, "New Procedure").object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_create_controller(self, objuuid):
        add_message("inventory controller: create controller: {0}".format(objuuid))
        try:
            return json.dumps(create_controller(objuuid, "New Controller").object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_create_rfc(self, objuuid):
        add_message("inventory controller: create RFC: {0}".format(objuuid))
        try:
            return json.dumps(create_rfc(objuuid, "New RFC").object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_create_link(self, objuuid):
        add_message("inventory controller: create link to {0}".format(objuuid))
        try:
            return json.dumps(create_link(objuuid).object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_delete(self, objuuid):
        add_message("inventory controller: delete inventory object: {0}".format(objuuid))
        try:
            while self.moving:
                sleep(.1)
            
            delete_node(objuuid)
            return json.dumps({"id" : objuuid})
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_context(self, objuuid):
        add_message("inventory controller: get context menu: {0}".format(objuuid))
        try:
            return json.dumps(get_context_menu(objuuid))
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_get_dependencies(self):
        add_message("inventory controller: get dependencies...")
        try:
            cl = cherrypy.request.headers['Content-Length']
            objuuids = json.loads(cherrypy.request.body.read(int(cl)))
            return json.dumps(get_dependencies(objuuids))
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_get_object(self, objuuid):
        add_message("inventory controller: get inventory object...")
        try:
            collection = Collection("inventory")
            object = collection.get_object(objuuid).object
            add_message("inventory controller: get: {0}, type: {1}, name: {2}".format(objuuid, object["type"], object["name"]))
            return json.dumps(object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_get_status_objects(self):
        add_message("inventory controller: get status objects...")
        try:
            return json.dumps(get_status_objects())
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def ajax_post_object(self):
        add_message("inventory controller: post inventory object...")
        
        try:
            cl = cherrypy.request.headers['Content-Length']
            object = json.loads(cherrypy.request.body.read(int(cl)))
        
            collection = Collection("inventory")
            current = collection.get_object(object["objuuid"])
            current.object = object
            current.set()
            
            add_message("inventory controller: set: {0}, type: {1}, name: {2}".format(object["objuuid"], object["type"], object["name"]))
        
            return json.dumps(current.object)
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def export_objects(self, objuuids):
        add_message("inventory controller: exporting inventory objects...")
        
        try:
            collection = Collection("inventory")
        
            inventory = {}
        
            for objuuid in objuuids.split(","):
                object = collection.get_object(objuuid).object
                
                if object["type"] != "container" and object["type"] != "link":
                    inventory[objuuid] = object
                    add_message("inventory controller: exported: {0}, type: {1}, name: {2}".format(objuuid, inventory[objuuid]["type"], inventory[objuuid]["name"]))
        
            cherrypy.response.headers['Content-Type'] = "application/x-download"
            cherrypy.response.headers['Content-Disposition'] = 'attachment; filename=export.{0}.json'.format(time())
        
            return serve_fileobj(json.dumps(inventory))
        except Exception:
            add_message(traceback.format_exc())
    
    @cherrypy.expose
    @require()
    def import_objects(self, file):
        add_message("inventory controller: importing inventory objects...")
        
        try:
            objects = json.loads(file.file.read())
            collection = Collection("inventory")
            
            container = create_container("#", "Imported Objects")
            
            existing_objuuids = collection.list_objuuids()
            
            for objuuid, object in objects.iteritems():
                current = collection.get_object(objuuid)
                
                parent = current.object["parent"]
                children = current.object["children"]
                
                current.object = object
                
                current.object["parent"] = parent
                current.object["children"] = children
                
                if objuuid not in existing_objuuids:
                    current.object["parent"] = container.objuuid
                    current.object["children"] = []
                    container.object["children"].append(objuuid)
                
                current.set()
            
                add_message("inventory controller: imported: {0}, type: {1}, name: {2}".format(objuuid, object["type"], object["name"]))
        
            if len(container.object["children"]) > 0:
                container.set()
            else:
                container.destroy()
            
        except Exception:
            add_message(traceback.format_exc())
        
        return json.dumps({})