#!/usr/bin/python
################################################################################
# IMPORT VALARIEDB METABASE
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 12/15/2016 Original construction
################################################################################

import sqlite3
import traceback

from .model.inventory import create_status_code, \
                             create_container, \
                             delete_node, \
                             create_task, \
                             create_rfc, \
                             create_procedure, \
                             set_parent_objuuid
                             
from .model.document import Collection

def import_metabase():
    inventory = Collection("inventory")
    current_objuuids = inventory.list_objuuids()
    
    metabase_container = inventory.get_object(create_container("#", "metabase")["objuuid"])

    conn = sqlite3.connect("metabase.db", 300)
    cur = conn.cursor()
    
    status_codes = []
    for status in inventory.find(type = "status"):
        try:
            status_codes.append(int(status.object["code"]))
        except Exception:
            print traceback.format_exc()
    
    cur.execute("select CODE, ALIAS, FRIENDLYTXT, TILETXT, CFGCOLOR, CBGCOLOR, SFGCOLOR, SBGCOLOR from STATUS;")
    conn.commit()
    
    status_container = inventory.get_object(create_container(metabase_container.objuuid, "Status Codes")["objuuid"])
    
    for row in cur.fetchall():
        if int(row[0]) not in status_codes:
            status = inventory.get_object(create_status_code(status_container.objuuid, row[2])["objuuid"])
            
            status.object["alias"] = row[1]
            status.object["code"] = str(row[0])
            status.object["abbreviation"] = row[3]
            status.object["cfg"] = str(row[4]).replace("#", "")
            status.object["cbg"] = str(row[5]).replace("#", "")
            status.object["sfg"] = str(row[6]).replace("#", "")
            status.object["sbg"] = str(row[7]).replace("#", "")
            
            status.set()
            
            print "imported status code: {0}, alias: {1}, name: {2}". \
                  format(status.object["code"], status.object["alias"], status.object["name"])

    

    
    cur.execute("select TSKUUID, BODY, NAME from TASK;")
    conn.commit()
    
    tasks_container = inventory.get_object(create_container(metabase_container.objuuid, "Tasks")["objuuid"])
    
    for row in cur.fetchall():
        if row[0] in current_objuuids:
            #delete_node(row[0])
            pass
        else:
            task = inventory.get_object(create_task(tasks_container.objuuid, row[2], row[0])["objuuid"])
        
            task.object["body"] = str(row[1]).replace("from globals import *", "")
        
            task.set()
        
            print "imported task name: {0}".format(task.object["name"])
    
    
    
    
    cur.execute("select RFCNUM, TITLE, DESCRIPTION, NAME, EMAIL, PHONE from RFC;")
    conn.commit()
    
    rfc_num_to_uuid = {}
    for rfc in inventory.find(type = "rfc"):
        try:
            rfc_num_to_uuid[(int(rfc.object["number"]))] = rfc.object["objuuid"]
        except Exception:
            print traceback.format_exc()
    
    rfcs_container = inventory.get_object(create_container(metabase_container.objuuid, "RFCs")["objuuid"])
    
    for row in cur.fetchall():
        if int(row[0]) in rfc_num_to_uuid:
            #delete_node(row[0])
            pass
        else:
            rfc = inventory.get_object(create_rfc(rfcs_container.objuuid, "")["objuuid"])
        
            rfc.object["description"] = row[2]
            rfc.object["title"] = row[1]
            rfc.object["poc name"] = row[3]
            rfc.object["poc phone"] = row[5]
            rfc.object["poc email"] = row[4]
            rfc.object["number"] = str(row[0])
            
            if row[1] == "":
                rfc.object["name"] = "RFC {0}".format(str(row[0]))
            else:
                rfc.object["name"] = "RFC {0} - {1}".format(str(row[0]), row[1])
            
            rfc.set()
        
            rfc_num_to_uuid[int(row[0])] = rfc.objuuid
        
            print "imported rfc number: {0}, name: {1}".format(rfc.object["number"], rfc.object["name"])
    
    
    
    
    
    cur.execute("select PRCUUID, NAME, TSKCONTINUE, TITLE, DISCUSSION from TBL_PROCEDURE;")
    conn.commit()
    
    procedures_container = inventory.get_object(create_container(metabase_container.objuuid, "Procedures")["objuuid"])
    
    for row in cur.fetchall():
        if row[0] in current_objuuids:
            #delete_node(row[0])
            pass
        else:
            procedure = inventory.get_object(create_procedure(procedures_container.objuuid, row[1], row[0])["objuuid"])
        
            procedure.object["title"] = row[3]
            procedure.object["description"] = row[4]
            
            for continue_code_str in row[2].split(","):
                try:
                    procedure.object["continue {0}".format(continue_code_str)] = "true"
                except Exception:
                    print traceback.format_exc()
            
            cur.execute("select TSKUUID from PROCSEQ where PRCUUID = ? order by SEQNUM;", (row[0],))
            conn.commit()
            for task_row in cur.fetchall():
                procedure.object["tasks"].append(task_row[0])
                
            cur.execute("select LNKUUID from PROCLNK where PRCUUID = ?;", (row[0],))
            conn.commit()
            for procedure_row in cur.fetchall():
                procedure.object["procedures"].append(procedure_row[0])
            
            cur.execute("select RFCNUM from RFC2PRCUUID where PRCUUID = ?;", (row[0],))
            conn.commit()
            for rfc_row in cur.fetchall():
                try:
                    procedure.object["rfcs"].append(rfc_num_to_uuid[int(rfc_row[0])])
                except Exception:
                    print traceback.format_exc()
        
            procedure.set()
            print "imported procedure name: {0}".format(procedure.object["name"])
            
            cur.execute("select TSKUUID from PROCSEQ where PRCUUID = ? order by SEQNUM;", (row[0],))
            conn.commit()
            for task_row in cur.fetchall():
                try:
                    print "moving task: {0}".format(task_row[0])
                    set_parent_objuuid(task_row[0], row[0])
                except Exception:
                    print traceback.format_exc()
        