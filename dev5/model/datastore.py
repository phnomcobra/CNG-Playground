#!/usr/bin/python
################################################################################
# DATASTORE
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 06/15/2017 Original construction
################################################################################

import traceback

from threading import Thread, Timer
from time import time, strftime, localtime

from .document import Collection

CHUNK_SIZE = 65536

def new_chunk():
    datastore = Collection("datastore")
    
    chunk = datastore.get_object()
    chunk.object = {
        "data" : bytearray(CHUNK_SIZE),
        "type" : "chunk",
    }
    chunk.set()
    
    return chunk

def new_sequence():
    datastore = Collection("datastore")
    
    sequence = datastore.get_object()
    sequence.object = {
        "chunks" : [],
        "size" : 0,
        "type" : "sequence"
    }
    sequence.set()
    
    return sequence
        
class Sequence:
    def __init__(self, sequuid = None):
        self.__position = 0
        self.__chunk_position = 0
        self.__datastore = Collection("datastore")
        self.__chunk = None
        self.__chunk_index = 0
        self.__end_of_sequence = False
        
        if sequuid in self.__datastore.find_objuuids(type = "sequence"):
            self.__sequence = self.__datastore.get_object(sequuid)
            self.__chunk = self.__datastore.get_object(self.__sequence.object["chunks"][0])
        else:
            self.__sequence = new_sequence()
            self.__chunk = new_chunk()
            self.__sequence.object["chunks"].append(self.__chunk.objuuid)
            self.__sequence.set()
        
    def seek(self, seek_position):
        if seek_position < 0 or seek_position >= self.__sequence.object["size"]:
            raise IndexError("Position out of bounds!")
        
        i = int(seek_position / CHUNK_SIZE)
        if self.__chunk_index != i:
            self.__chunk.set()
            self.__chunk = self.__datastore.get_object(self.__sequence.object["chunks"][i])
            self.__chunk_index = i
            
        self.__chunk_position = seek_position % CHUNK_SIZE
        
        self.__position = seek_position
        
        self.__end_of_sequence = False
    
    def read(self, num_bytes = None):
        buffer = bytearray()
        
        if self.__end_of_sequence == True:
            pass
        elif num_bytes == None:
            for i in range(self.__position, self.__sequence.object["size"]):
                buffer.append(self.__chunk.object["data"][self.__chunk_position])
                
                try:
                    self.seek(1 + self.__position)
                except IndexError:
                    self.__end_of_sequence = True
                    break
        else:
            for i in range(self.__position, self.__position + num_bytes):
                buffer.append(self.__chunk.object["data"][self.__chunk_position])
                
                try:
                    self.seek(1 + self.__position)
                except IndexError:
                    self.__end_of_sequence = True
                    break
        
        return buffer        
    
    def resize(self, num_bytes):
        self.__sequence.object["size"] = num_bytes
        
        num_chunks = int(num_bytes / CHUNK_SIZE) + 1
        num_chunks_exist = len(self.__sequence.object["chunks"])
        
        if num_chunks_exist < num_chunks:
            for i in range(num_chunks_exist, num_chunks):
                chunk = new_chunk()
                self.__sequence.object["chunks"].append(chunk.objuuid)
        else:
            for i in range(num_chunks_exist, num_chunks, -1):
                self.__datastore.get_object(self.__sequence.object["chunks"][i]).destroy()
                self.__sequence.object["chunks"].pop()
        
        self.__sequence.set()
    
    def write(self, raw_buffer):
        buffer = bytearray()
        
        buffer.extend(raw_buffer)
        
        if self.__end_of_sequence == True:
            pass
        else:
            for i in range(0, len(buffer)):
                self.__chunk.object["data"][self.__chunk_position] = buffer[i]

                try:
                    self.seek(1 + self.__position)
                except IndexError:
                    self.__end_of_sequence = True
                    break
        
            self.__chunk.set()

collection = Collection("datastore")
collection.create_attribute("type", "['type']")

