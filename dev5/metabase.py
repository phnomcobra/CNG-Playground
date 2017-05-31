#!/usr/bin/python
################################################################################
# VALARIEDB METABASE CONVERSION
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 12/28/2016 Original construction
################################################################################

import sqlite3
import traceback

from .model.inventory import create_container, \
                             delete_node, \
                             create_task, \
                             create_rfc, \
                             create_link, \
                             create_procedure, \
                             set_parent_objuuid
                             
from .model.document import Collection

inventory = Collection("inventory")
current_objuuids = inventory.list_objuuids()

conn = sqlite3.connect("metabase.db", 300)
cur = conn.cursor()

rfc_num_to_uuid = {}
tskuuids = []
prcuuids = []

def load():
    metabase_container = create_container("#", "metabase")

    rfcs_container = create_container(metabase_container.objuuid, "RFCs")
    
    cur.execute("select RFCNUM, TITLE, DESCRIPTION, NAME, EMAIL, PHONE from RFC;")
    conn.commit()

    for row in cur.fetchall():
        rfc = create_rfc(rfcs_container.objuuid)
        
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

    
    
    cur.execute("select CTRUUID, NAME from CONTROLLER;")
    conn.commit()
    
    controllers_container = create_container(metabase_container.objuuid, "Controllers")
    tasks_container = create_container(metabase_container.objuuid, "Tasks")
    procedures_container = create_container(metabase_container.objuuid, "Procedures")
    
    for row in cur.fetchall():
        if row[0] in current_objuuids:
            #delete_node(row[0])
            pass
        else:
            controller_container = create_container(controllers_container.objuuid, row[1])
            procedure_links_container = create_container(controller_container.objuuid, "Procedure Links")
            related_links_container = create_container(controller_container.objuuid, "Related Procedure Links")
            
            cur.execute("select distinct PRCUUID from CONTSEQ where CTRUUID = ?;", (row[0],))
            conn.commit()
            for procedure_row in cur.fetchall():
                try:
                    load_procedure(procedure_row[0], procedures_container.objuuid, tasks_container)
                    create_link(procedure_row[0], procedure_links_container.objuuid)
                except Exception:
                    print traceback.format_exc()
                
                cur.execute("select distinct LNKUUID from PROCLNK where PRCUUID = ?;", (procedure_row[0],))
                conn.commit()
                for rel_procedure_row in cur.fetchall():
                    try:
                        load_procedure(rel_procedure_row[0], procedures_container.objuuid, tasks_container)
                        create_link(rel_procedure_row[0], related_links_container.objuuid)
                    except Exception:
                        print traceback.format_exc()
            
            print "imported controller: {0}".format(row[1])

def load_procedure(prcuuid, parent_objuuid, tasks_container):
    cur.execute("select NAME, TSKCONTINUE, TITLE, DISCUSSION from TBL_PROCEDURE where PRCUUID = ?;", (prcuuid,))
    conn.commit()
    row = cur.fetchall()[0]

    if prcuuid not in prcuuids:
        prcuuids.append(prcuuid)
        procedure = create_procedure(parent_objuuid, row[0], prcuuid)
        
        procedure.object["title"] = row[2]
        procedure.object["description"] = row[3]
            
        for continue_code_str in row[1].split(","):
            try:
                procedure.object["continue {0}".format(continue_code_str)] = "true"
            except Exception:
                print traceback.format_exc()
            
        cur.execute("select TSKUUID from PROCSEQ where PRCUUID = ? order by SEQNUM;", (prcuuid,))
        conn.commit()
        for task_row in cur.fetchall():
            procedure.object["tasks"].append(task_row[0])
            if task_row[0] not in tskuuids:
                tskuuids.append(task_row[0])
                load_task(task_row[0], tasks_container.objuuid)
    
        cur.execute("select distinct RFCNUM from RFC2PRCUUID where PRCUUID = ?;", (prcuuid,))
        conn.commit()
        for rfc_row in cur.fetchall():
            try:
                if rfc_num_to_uuid[int(rfc_row[0])] not in procedure.object["rfcs"]:
                    procedure.object["rfcs"].append(rfc_num_to_uuid[int(rfc_row[0])])
            except Exception:
                print traceback.format_exc()
        
        procedure.set()
        print "imported procedure name: {0}".format(procedure.object["name"])
    
        return procedure
    else:
        return inventory.get_object(prcuuid)

def load_task(tskuuid, parent_objuuid):
    cur.execute("select BODY, NAME from TASK where TSKUUID = ?;", (tskuuid,))
    conn.commit()
    row = cur.fetchall()[0]
    
    task = create_task(parent_objuuid, row[1], tskuuid)
        
    task.object["body"] = str(row[0]).replace("from globals import *", "")
        
    task.set()
        
    print "imported task name: {0}".format(task.object["name"])
    
    return task