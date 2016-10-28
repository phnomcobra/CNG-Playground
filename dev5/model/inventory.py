#!/usr/bin/python
################################################################################
# INVENTORY
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/28/2016 Original construction
################################################################################

import sqlite3

from .utils import sucky_uuid

class Inventory:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite", 300)
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS TBL_INVENTORY (
                               PARUUID VARCHAR(36) REFERENCES TBL_INVENTORY(ITMUUID),
                               OBJUUID VARCHAR(36) REFERENCES TBL_OBJECT_PROTO(OBJUUID) NOT NULL,
                               ITMUUID VARCHAR(36) NOT NULL,
                               POSITION INTEGER NOT NULL DEFAULT 0,
                               NAME VARCHAR(64) DEFAULT 'New Item',
                               PRIMARY KEY (ITMUUID))''')
        

        self.connection.commit()
        
        self.get_objects()
    
    def __del__(self):
        self.connection.close()
    
    def create_prototype(self, uuid = sucky_uuid(), name = "New Object Prototype"):
        try:
            self.cursor.execute("insert into TBL_OBJECT_PROTO (OBJUUID, NAME) values (?, ?);", \
                                (str(uuid), str(name)))
            self.connection.commit()
            
            self.get_objects()
            
            return {"uuid" : uuid, "name" : name}
        except Exception as e:
            return {"exception" : e}
    
    def delete_prototype(self, uuid):
        try:
            self.cursor.execute("delete from TBL_OBJECT_PROTO where OBJUUID = ?);", \
                                (str(uuid),))
            self.connection.commit()
            
            self.get_objects()
            
            return {}
        except Exception as e:
            return {"exception" : e}
    
    def rename_prototype(self, uuid, name):
        try:
            self.cursor.execute("update TBL_OBJECT_PROTO set NAME = ? where OBJUUID = ?);", \
                                (str(name), str(uuid)))
            self.connection.commit()
            
            self.get_objects()
            
            return {"uuid" : uuid, "name" : name}
        except Exception as e:
            return {"exception" : e}
    
    def create_reference(self, uuid, creates_uuid):
        try:
            self.cursor.execute("insert into TBL_OBJECT_XREF (OBJUUID, CREATES) values (?, ?);", \
                                (str(uuid), str(creates_uuid)))
            self.connection.commit()
            
            self.get_objects()
            
            return {"uuid" : uuid, "creates_uuid" : creates_uuid}
        except Exception as e:
            return {"exception" : e}

    def delete_reference(self, uuid, creates_uuid):
        try:
            self.cursor.execute("delete from TBL_OBJECT_XREF where OBJUUID = ? and CREATES = ?;", \
                                (str(uuid), str(creates_uuid)))
            self.connection.commit()
            
            self.get_objects()
            
            return {}
        except Exception as e:
            return {"exception" : e}
    
    def get_objects(self):
        try:
            self.cursor.execute("select OBJUUID, NAME from TBL_OBJECT_PROTO;")
            self.connection.commit()
            
            self.objects = {}
            for object_proto_row in self.cursor.fetchall():
                self.objects[object_proto_row[0]] = {"name" : object_proto_row[1], "creates" : {}}
                
                self.cursor.execute("""select T2.OBJUUID, T2.NAME from TBL_OBJECT_XREF T1, TBL_OBJECT_PROTO T2 
                                       on T1.CREATES = T2.OBJUUID 
                                       where T1.OBJUUID = ?;""", (object_proto_row[0],))
                self.connection.commit()
                
                for object_xref_row in self.cursor.fetchall():
                    self.objects[object_proto_row[0]]["creates"][object_xref_row[0]] = {"name" : object_xref_row[1]}
            
            return {}
        except Exception as e:
            return {"exception" : e}