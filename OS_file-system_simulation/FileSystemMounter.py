#!/usr/bin/python
'''This module mounts the fileSystem in the main Memory
    dependancy:
    1) FileOperator (lower level file handling Functionality)
    2) RLBB (The lookaside buffer Functionality)
    This is then used by main interpreter script'''

# coded by botMan

from FileOperator import Operator # the lower level fileSystem Functionality module
from RLBB import CacheBuffer # the lookaside buffer Functionality modules

class FileSystemMounter(object):
    ''' Class that mounts the fileSystem in the main memory '''

    def __init__(self):
        ''' Default Constructor of the class '''
        self.fileSystemStructure = {} # initialize to empty dictionary

    def __remount(self):
        '''Remount the file system'''
        self.fileSystemStructure = {} # clear all the contents of the dictionary
        self.mount()

    def mount(self):
        ''' Mounts the Text based fileSystem'''
        size = int(Operator.readFile(2, 0)[0].split("=")[1]) # get the current size of the metadata block

        # read the metadata block and setup the dictionary
        lines = Operator.readFile(3, size)
        for line in lines:
            nodes = line.split(" ")[2:]
            for node in nodes:
                # filll in the fileSystemStructure with the fileNodes
                details = node[1:len(node)-1].split(",")
                self.fileSystemStructure[details[0]] = (int(details[1]), int(details[2]))

    def readFile(self, filename): # throws file not found exception
        ''' Read the required file'''
        # check if the file exists
        if filename not in self.fileSystemStructure:
            raise Exception("\nERROR: FILE NOT FOUND\n")

        try:
            # check in the CacheBuffer first
            contents = CacheBuffer.searchEntry(filename)
        except Exception as exc:
            # else fetch from the File
            node = self.fileSystemStructure[filename]
            contents = Operator.readFile(node[0], node[1])

            # add an entry to the cache buffer
            CacheBuffer.addEntry(filename, contents)

        finally:
            return contents

    def addFile(self, filename, contents): # throws file already Exists exception
        '''Add a new file in the FileSystem'''
        if filename in self.fileSystemStructure:
            raise Exception("\nERROR: FILE ALREADY EXISTS\n")

        # delayed Write Functionality not implemented yet
        # so the file is directly added to the FileSystem
        Operator.addFile(filename, contents) # Write the file
        self.__remount() # remount the fileSystem

    def deleteFile(self, filename): # throws file not found exception
        '''delete a file from FileSystem'''
        if filename not in self.fileSystemStructure:
            raise Exception("\nERROR: FILE NOT FOUND\n")

        # delayed Write Functionality not implemented yet
        # so the file is directly deleted from the FileSystem
        Operator.deleteFile(filename) # remove the file
        self.__remount() # remount the fileSystem

    def listFiles(self):
        '''Return all the filenames in the fileSystem'''
        return self.fileSystemStructure.keys()


Mounter = FileSystemMounter() # object created for the plug and play feature

# test script starts here
'''Remounter works'''
# Mounter.mount()
# Operator.deleteFile("stu.txt")
# print "\nThis is remount output: "
# Mounter.remount()

'''ReadFile Works'''
# Mounter.readFile("ghi.txt")
# print CacheBuffer.lookAsideBuffer

'''Delete File works'''
# Mounter.deleteFile("yz.txt")
# print Mounter.fileSystemStructure

'''Add File Works'''
# try:
#     Mounter.addFile("man.txt", ["My name is Batman!!", "And my mother's name is MARTHA"])
#     print Mounter.fileSystemStructure
# except Exception as exc:
#     print exc
