#!/usr/bin/python
''' This module provides the Lookaside Buffer Functionality to the TextFS
    The name of the module has been kept as R Look Bajula Buffer. R is a
    pun on the word Our'''

''' All the tests clear for now '''

# coded by botMan

import time # time library for the timestamp

class RLBB(object):
    '''Clas for the fast lookaside buffer'''

    def __init__(self):
        '''Constructor for the class'''
        self.lookAsideBuffer = {} # empty dictionary for the buffer
        self.bufferSize = 5 # current default value for the buffersize
        self.currentSize = 0 # current size of the buffer

    def __deleteEntry(self): # private method
        '''Delete the least recently used entry in the buffer'''
        # find the least recently used entry below
        deleteEntry = min(self.lookAsideBuffer.items(), key = lambda x: x[1][0])[0]
        self.lookAsideBuffer.pop(deleteEntry) # remove the least recently used entry

    def setBufferSize(self, newSize):
        '''Change the Buffer Size as required'''
        self.bufferSize = newSize

    def searchEntry(self, filename): # throws "File not found" Exception
        if(self.lookAsideBuffer.has_key(filename)):
            self.lookAsideBuffer[filename][0] = time.time() # update the timestamp
            return self.lookAsideBuffer[filename][1] # return the contents
        raise Exception("File not in Buffer") # otherwise raise an exception

    def addEntry(self, filename, contents):
        ''' Add an Entry in the buffer from the textFS'''
        timestamp = time.time() # record the current time as a timestamp
        if(self.currentSize == self.bufferSize):
            # case when the buffer is full
            self.__deleteEntry()

        self.lookAsideBuffer[filename] = [timestamp, contents] # simply add a file
        # the above pair has been kept as a list not tuple because the timestamp
        # will Change if the file is read and tuple is immutable

        self.currentSize += 1 # increment the current size of the buffer


CacheBuffer = RLBB() # Object created for the plug and play feature

# # test script here:
# testObj = RLBB()
# testObj.setBufferSize(2)
# testObj.addEntry("abc.txt", "HELLO WORLD")
# testObj.addEntry("def.txt", "HELLO WORLD")
# print testObj.lookAsideBuffer
# testObj.addEntry("ghi.txt", "HELLO WORLD")
# print testObj.lookAsideBuffer
# try:
#     print testObj.searchEntry("def.txt")
#     print testObj.searchEntry("abc.txt")
# except Exception as err:
#     print(repr(err))
