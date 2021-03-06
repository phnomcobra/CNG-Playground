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

def new_sequence(sequuid = None):
    datastore = Collection("datastore")
    
    sequence = datastore.get_object(sequuid)
    sequence.object = {
        "chunks" : [],
        "size" : 0,
        "type" : "sequence"
    }
    sequence.set()
    
    return sequence

def delete_sequence(sequuid):
    datastore = Collection("datastore")
    
    sequence = datastore.get_object(sequuid)
    
    if "chunks" in sequence.object:
        for chunkid in sequence.object["chunks"]:
            datastore.get_object(chunkid).destroy()
    
    sequence.destroy()
    
class File:
    def __init__(self, sequuid = None):
        self.__position = 0L
        self.__chunk_position = 0
        self.__datastore = Collection("datastore")
        self.__chunk = None
        self.__chunk_index = 0
        self.__chunk_changed = False
        self.__end_of_sequence = False
        self.__following_write = False
        
        if sequuid in self.__datastore.find_objuuids(type = "sequence"):
            self.__sequence = self.__datastore.get_object(sequuid)
            self.__chunk = self.__datastore.get_object(self.__sequence.object["chunks"][0])
        else:
            self.__sequence = new_sequence(sequuid)
            self.__chunk = new_chunk()
            self.__sequence.object["chunks"].append(self.__chunk.objuuid)
            self.__sequence.set()
    
    def __del__(self):
        self.close()
    
    def tell(self):
        return self.__position
    
    def size(self):
        return self.__sequence.object["size"]
    
    def close(self):
        self.__sequence.set()
        self.__chunk.set()
    
    def open(self, **kargs):
        self.__init__(kargs)
    
    def fileno(self):
        return 0
    
    def seek(self, seek_position):
        if seek_position < 0 or seek_position >= self.__sequence.object["size"]:
            raise IndexError("Position out of bounds!")
        
        i = int(seek_position / CHUNK_SIZE)
        if self.__chunk_index != i:
            if self.__chunk_changed == True:
                self.__chunk.set()
                
            self.__chunk = self.__datastore.get_object(self.__sequence.object["chunks"][i])
            self.__chunk_index = i
            
            self.__chunk_changed = False
            
        self.__chunk_position = seek_position % CHUNK_SIZE
        
        self.__position = seek_position
        
        self.__following_write = False
        
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

    def next(self):        
        buffer = bytearray()
        
        if self.__end_of_sequence == True:
            raise StopIteration("End of file!")
        else:
            b = b''
            
            while b != b'\n':
                b = self.__chunk.object["data"][self.__chunk_position]
                
                buffer.append(b)
                
                try:
                    self.seek(1 + self.__position)
                except IndexError:
                    self.__end_of_sequence = True
                    break
        
        return buffer

    def readline(self, num_bytes = None):        
        buffer = bytearray()
        
        if self.__end_of_sequence == True:
            pass
        else:
            b = b''
            c = 0L
            
            while b != b'\n':
                b = self.__chunk.object["data"][self.__chunk_position]
                
                buffer.append(b)
                c += 1
                
                if numbytes != None and \
                   numbytes >= 0 and \
                   numbytes == c:
                    break
                
                try:
                    self.seek(1 + self.__position)
                except IndexError:
                    self.__end_of_sequence = True
                    break
                
        
        return buffer
    
    def readlines(self, num_bytes = None):        
        buffers = []
        buffer = bytearray()
        
        if self.__end_of_sequence == True:
            pass
        else:
            b = b''
            c = 0L
            
            while b != b'\n':
                b = self.__chunk.object["data"][self.__chunk_position]
                
                buffer.append(b)
                c += 1
                
                if numbytes != None and \
                   numbytes >= 0 and \
                   numbytes == c:
                    buffers.append(buffer)
                    buffer = bytearray()
                    c = 0L
                
                try:
                    self.seek(1 + self.__position)
                except IndexError:
                    self.__end_of_sequence = True
                    break
        
        buffers.append(buffer)
        
        return buffers
    
    def truncate(self, num_bytes = None):
        if num_bytes == None:
            self.resize(self.__position + 1)
        else:
            self.resize(num_bytes)
    
    def flush(self):
        pass
    
    def isatty(self):
        return False
    
    def resize(self, num_bytes):
        self.__sequence.object["size"] = num_bytes
        
        num_chunks = int(num_bytes / CHUNK_SIZE) + 1
        num_chunks_exist = len(self.__sequence.object["chunks"])
        
        if num_chunks_exist < num_chunks:
            for i in range(num_chunks_exist, num_chunks):
                chunk = new_chunk()
                self.__sequence.object["chunks"].append(chunk.objuuid)
        else:
            for i in range(num_chunks_exist - 1, num_chunks - 1, -1):
                self.__datastore.get_object(self.__sequence.object["chunks"][i]).destroy()
                self.__sequence.object["chunks"].pop()
    
    def writelines(raw_buffer_list):
        for raw_buffer in raw_buffer_list:
            self.write(raw_buffer)
    
    def write(self, raw_buffer):
        buffer = bytearray()
        
        buffer.extend(raw_buffer)
        
        if self.__following_write == True and \
           len(buffer) > 0 and \
           self.size() < self.__position + len(buffer) + 2:
            self.resize(self.__position + len(buffer) + 1)
            self.seek(1 + self.__position)
        elif self.__following_write == False and \
             len(buffer) > 0 and \
             self.size() < self.__position + len(buffer) + 1:
            self.resize(self.__position + len(buffer) + 1)
        
        for i in range(0, len(buffer)):
            self.__chunk.object["data"][self.__chunk_position] = buffer[i]
            self.__chunk_changed = True
            
            if i < len(buffer) - 1:
                self.seek(1 + self.__position)
        
        self.__following_write = True
collection = Collection("datastore")
collection.create_attribute("type", "['type']")

