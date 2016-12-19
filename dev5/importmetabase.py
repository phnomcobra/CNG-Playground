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
                             set_parent_objuuid, \
                             create_host, \
                             create_controller, \
                             create_console
                             
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
                
            cur.execute("select distinct LNKUUID from PROCLNK where PRCUUID = ?;", (row[0],))
            conn.commit()
            for procedure_row in cur.fetchall():
                if procedure_row[0] not in procedure.object["procedures"]:
                    procedure.object["procedures"].append(procedure_row[0])
            
            cur.execute("select distinct RFCNUM from RFC2PRCUUID where PRCUUID = ?;", (row[0],))
            conn.commit()
            for rfc_row in cur.fetchall():
                try:
                    if rfc_num_to_uuid[int(rfc_row[0])] not in procedure.object["rfcs"]:
                        procedure.object["rfcs"].append(rfc_num_to_uuid[int(rfc_row[0])])
                except Exception:
                    print traceback.format_exc()
        
            procedure.set()
            print "imported procedure name: {0}".format(procedure.object["name"])
            
            cur.execute("select distinct TSKUUID from PROCSEQ where PRCUUID = ? order by SEQNUM;", (row[0],))
            conn.commit()
            for task_row in cur.fetchall():
                try:
                    print "moving task: {0}".format(task_row[0])
                    #set_parent_objuuid(task_row[0], row[0])
                except Exception:
                    print traceback.format_exc()
            
            cur.execute("select distinct RFCNUM from RFC2PRCUUID where PRCUUID = ?  limit 1;", (row[0],))
            conn.commit()
            for rfc_row in cur.fetchall():
                try:
                    print "moving RFC: {0}".format(task_row[0])
                    #set_parent_objuuid(rfc_num_to_uuid[int(rfc_row[0])], row[0])
                except Exception:
                    print traceback.format_exc()
    
    
    consoles_container = inventory.get_object(create_container(metabase_container.objuuid, "Consoles")["objuuid"])
    
    ssh_console = inventory.get_object(create_console(consoles_container.objuuid, "SSH", "99225302-9d6e-8806-0165-d467eb4d3323")["objuuid"])
        
    ssh_console.object["body"] = '''#!/usr/bin/python
################################################################################
# SSH CLI
# 
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# SSH command line interface class. This class is a wrapper for os.popen. Each
# console object maitains a continuous ssh session to the specified remote host
# using specified credentials.
#
# 12/10/2014 Original construction
# 12/18/2014 Added mysql method
# 12/31/2014 Added cmp_mysql_password method
#            Added cmp_mysql_username method
#            Modified system method to concatanate stderr and stdout if status
#            is not 0
# 01/05/2015 Added return tuple parameter to system
#            Added sftp member
# 01/07/2015 Applied replace("[sudo] password for " + self.__username + ":", "")
#            to stderr and stdout buffers
# 01/12/2015 Applied replace to stderr buffer
# 01/14/2015 Changed mysql method to run without sudo and supply the mysql
#               password through stdin interactively. This is a fix for the
#               mysql credentials being exposed in /var/log/secure.
# 02/17/2015 Allowed MySQL credentials to be overridded with optional parameters
#               supplied to the MySQL method.
# 04/24/2015 Updated string formatting to shift away from += and + operators for
#               long strings.
# 04/27/2015 Added MySQL dump and MySQL batch methods.
#            Return tuple optional parameter has been added to the Mysql 
#               methods.
# 08/07/2015 Adjusted formatting statements to be compatible with Python 2.6.6
# 08/17/2015 Added get_shell method for asynchronous channel interaction
# 09/01/2015 Removed sudo testing from connect method
# 10/05/2015 Added optional parameter to system to defer from elevating to sudo.
# 10/14/2015 Added session variables and extended logging
# 01/27/2016 Added RSA key based auth
# 04/26/2016 Added lossy ascii character set conversion to mysql and system
#               methods
# 05/23/2016 Added password inspection methods
# 09/07/2016 Added SSH forwarding for MySQL.
# 09/12/2016 Added SSH tunnel methods.
################################################################################

import paramiko
import pymysql
import select

from time import time
from threading import Thread
from random import randrange

import socket
import SocketServer

class ForwardServer (SocketServer.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True

def verbose(text):
    #print text
    pass
    
class Handler (SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            chan = self.ssh_transport.open_channel('direct-tcpip',
                                                   (self.chain_host, self.chain_port),
                                                   self.request.getpeername())
        except Exception as e:
            verbose('Incoming request to %s:%d failed: %s' % (self.chain_host,
                                                              self.chain_port,
                                                              repr(e)))
            return
        if chan is None:
            verbose('Incoming request to %s:%d was rejected by the SSH server.' %
                    (self.chain_host, self.chain_port))
            return

        verbose('Connected!  Tunnel open %r -> %r -> %r' % (self.request.getpeername(),
                                                            chan.getpeername(), (self.chain_host, self.chain_port)))
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)
                
        peername = self.request.getpeername()
        chan.close()
        self.request.close()
        verbose('Tunnel closed from %r' % (peername,))

class Console:
    def __init__(self, **kargs):
        # Private Members
        self.__ssh = paramiko.SSHClient()
        self.__username = kargs["session"]["ssh username"]
        self.__password = kargs["session"]["ssh password"]
        self.__private_key = None
        self.__remote = kargs["host"]
        self.__mysql_username = kargs["session"]["mysql username"]
        self.__mysql_password = kargs["session"]["mysql password"]
        self.__mysql_remote = None
        self.__session_var = {}
        self.__tunnel = {}
        
        # Public Members
        self.sftp = None

    #### Mutation Methods ########################
    def set_username(self, username):
        self.__username = username
        
    def set_password(self, password):
        self.__password = password
    
    def set_private_key(self, key_filename, password = None):
        self.__private_key = paramiko.RSAKey.from_private_key_file(key_filename, password = password)

    def set_remote_host(self, remote):
        self.__remote = remote
    
    def set_mysql_username(self, username):
        self.__mysql_username = username
        
    def set_mysql_password(self, password):
        self.__mysql_password = password
        
    def set_mysql_remote(self, remote):
        self.__mysql_remote = remote
    
    #### Set Key Value ###########################
    def set(self, key, value):
        try:
            self.__session_var[key] = value
        except Exception:
            self.__session_var = {}
            self.__session_var[key] = value
    
    #### Inspection Methods ######################
    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password
    
    def get_remote_host(self):
        return self.__remote
    
    def get_mysql_username(self):
        return self.__mysql_username
    
    def get_mysql_password(self):
        return self.__mysql_password
        
    def get_mysql_remote(self):
        return self.__mysql_remote
    
    #### Get Key Value ###########################
    # Return key value. If a key error exception is thrown, return none.
    def get(self, key):
        try:
            value = self.__session_var[key]
            return value
        except Exception as e:
            return None
    
    #### Test sudo ###############################
    # Test sudo by sudoing whoami. Credentials are fed into standard input and
    # flushed after executing sudo. If a non-zero return code is recieved a
    # custom exception is raised.
    def __test_sudo(self):
        if not self.__username == "root":
            stdin, stdout, stderr = self.__ssh.exec_command('sudo -S whoami')
            stdin.write(self.__password + '\n')
            stdin.flush()
            if 0 != int(stdout.channel.recv_exit_status()):
                raise NameError('Sudo test failed with {0}@{1}'.format(self.__username, self.__remote))
    
    #### Connect to SSH Server ###################
    # Set host key policy to AutoAddPolicy() and connect to host using credentials
    # from private members. Finally test sudo.
    def connect(self):
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.__private_key:        
            self.__ssh.connect(self.__remote, username = self.__username, pkey = self.__private_key)
        else:
            self.__ssh.connect(self.__remote, username = self.__username, password = self.__password)
        self.__ssh.get_transport().set_keepalive(30)
        self.sftp = self.__ssh.open_sftp()
    
    #### Close Connection ########################
    # Close SFTP and SSH connections
    def close(self):
        self.sftp.close()
        self.__ssh.close()
    
    #### Get Shell ###############################
    # Return channel object for an interactive shell
    def get_shell(self):
        return self.__ssh.invoke_shell()

    #### System Command ##########################
    # Execute command on SSHClient. If the credentials has a user other than root
    # append the command into a sudo command. If redirection is used with sudo,
    # run the command in its own bash shell to preserve privileges while
    # redirecting to a file. If __debug is set to true, print all three I/O
    # streams during execution. If a non-zero exit code is returned, tag the
    # standard error buffer as red font and add it to the output buffer. If the
    # return tuple parameter is set to true, a tuple of the exit status, standard
    # output buffer, and standard error buffer is returned.
    def system(self, command, return_tuple = False, sudo_command = True):
        if self.__username == "root" or not sudo_command:
            stdin, stdout, stderr = self.__ssh.exec_command(command)
        else:
            if " > " in command or " >> " in command:
                stdin, stdout, stderr = self.__ssh.exec_command("sudo -S bash -c '{0}'".format(command))
            else:
                stdin, stdout, stderr = self.__ssh.exec_command('sudo -S ' + command)
            stdin.write(self.__password + '\n')
            stdin.flush()

        # Lossy ascii character set conversion
        output_buffer = ""
        for c in stdout.read().replace("[sudo] password for {0}:".format(self.__username), ""):
            try:
                output_buffer += c.encode("ascii", "ignore")
            except Exception:
                pass

        # Lossy ascii character set conversion
        stderr_buffer = ""
        for c in stderr.read().replace("[sudo] password for {0}:".format(self.__username), ""):
            try:
                stderr_buffer += c.encode("ascii", "ignore")
            except Exception:
                pass
        
        status = stdout.channel.recv_exit_status()
        
        if return_tuple:
            return status, output_buffer, stderr_buffer
        elif 0 != int(status):
            return '{0}<font color="red"><br>{1}</font><br>'.format(output_buffer, stderr_buffer)
        else:
            return output_buffer
    
    #### SSH Tunnel ##############################
    # Methods for starting and stopping SSH tunnels. 
    def __start_tunnel(self, local_port, remote_host, remote_port):
        transport = self.__ssh.get_transport()
        class SubHandler (Handler):
            chain_host = remote_host
            chain_port = remote_port
            ssh_transport = transport
        self.__tunnel[local_port] = ForwardServer(('', local_port), SubHandler)
        self.__tunnel[local_port].serve_forever()
    
    def start_tunnel(self, local_port, remote_host, remote_port):    
        Thread(target = self.__start_tunnel, args = (local_port, remote_host, remote_port)).start()
    
    def stop_tunnel(self, local_port):
        self.__tunnel[local_port].shutdown()
        del self.__tunnel[local_port]
    
    #### MySQL Query #############################
    # Assemble a MySQL batch query using the MySQL remote host and credentials
    # members. If the remote host is set to none, assume localhost when
    # running the query. MySQL credentials can be overridded as optional 
    # parameters supplied to the mysql method. Original method has been 
    # overhauled to forward pymysql connections over SSH rather than using
    # remote clients.
    def mysql(self, \
              query, \
              password = None, \
              username = None, \
              mysql_remote = None, \
              return_tuple = False):
        if not password:
            password = self.__mysql_password

        if not username:
            username = self.__mysql_username

        if not mysql_remote:
            mysql_remote = self.__mysql_remote

        if not username or not password:
            raise Exception('MySQL query attempted without credentials set.')
        
        try:
            local_port = randrange(0, 1000, 1) + 50000
            self.start_tunnel(local_port, mysql_remote, 3306)
            
            conn = pymysql.connect(host = "127.0.0.1", port = local_port, user = username, passwd = password)
            cur = conn.cursor()

            try:
                cur.execute(query)
                conn.commit()
                
                output_buffer = ""
                for row in cur.fetchall():
                    output_buffer += "\n"
                    for i, col in enumerate(row):
                        output_buffer += str(col)
                        if i < len(row) - 1:
                            output_buffer += "\t"
                    
                stderr_buffer = ""
                status = 0
            except Exception as e:
                output_buffer = ""
                stderr_buffer = str(e)
                status = 1
            
            conn.close()
        except Exception as e:
            output_buffer = ""
            stderr_buffer = str(e)
            status = 1
        finally:
            self.stop_tunnel(local_port)
        
        if return_tuple:
            return status, output_buffer, stderr_buffer
        elif 0 != int(status):
            return '{0}<font color="red"><br>{1}</font><br>'.format(output_buffer, stderr_buffer)
        else:
            return output_buffer
        
    def cmp_mysql_password(self, password):
        return password == self.__mysql_password

    def cmp_mysql_username(self, username):
        return username == self.__mysql_username'''
    
    ssh_console.set()
    
    print "imported SSH console..."
    
    
    
    cur.execute("select HSTUUID, HOST, NAME from HOST;")
    conn.commit()
    
    hosts_container = inventory.get_object(create_container(metabase_container.objuuid, "Hosts")["objuuid"])
    
    for row in cur.fetchall():
        if row[0] in current_objuuids:
            #delete_node(row[0])
            pass
        else:
            host = inventory.get_object(create_host(hosts_container.objuuid, row[2], row[0])["objuuid"])
        
            host.object["host"] = row[1]
            host.object["console"] = ssh_console.objuuid
        
            host.set()
        
            print "imported host: {0}, name: {1}".format(host.object["host"], host.object["name"])

    
    
    
    
    cur.execute("select CTRUUID, NAME from CONTROLLER;")
    conn.commit()
    
    controllers_container = inventory.get_object(create_container(metabase_container.objuuid, "Controllers")["objuuid"])
    
    for row in cur.fetchall():
        if row[0] in current_objuuids:
            #delete_node(row[0])
            pass
        else:
            controller = inventory.get_object(create_controller(controllers_container.objuuid, row[1], row[0])["objuuid"])
            
            cur.execute("select distinct HSTUUID from CONTHST where CTRUUID = ?;", (row[0],))
            conn.commit()
            for host_row in cur.fetchall():
                if host_row[0] not in controller.object["hosts"]:
                    controller.object["hosts"].append(host_row[0])
            
            cur.execute("select distinct PRCUUID from CONTSEQ where CTRUUID = ?;", (row[0],))
            conn.commit()
            for procedure_row in cur.fetchall():
                if procedure_row[0] not in controller.object["procedures"]:
                    controller.object["procedures"].append(procedure_row[0])
        
            controller.set()
            
            cur.execute("select distinct PRCUUID from CONTSEQ where CTRUUID = ?;", (row[0],))
            conn.commit()
            for procedure_row in cur.fetchall():
                #set_parent_objuuid(procedure_row[0], row[0])
                print "moving procedure: {0}".format(procedure_row[0])
        
            print "imported controller: {0}".format(controller.object["name"])