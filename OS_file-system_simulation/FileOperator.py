#!/usr/bin/python
'''This module provides the lower level file handling Functionality
    This is then used by the mounted file system and the RLBB'''

# coded by botMan

import linecache # fast line based file reading library
import os # the operating sysem library

class FileOperator(object):
    '''Class for the lower level Functionality in TextFS'''

    # end of block denoter
    global EOB, SOF
    SOF = "================================================================================"
    EOB = "################################################################################\n"

    def __init__(self, fileSystem):
        ''' Constructor for the class'''
        self.FILE_SYSTEM = fileSystem # the single TextFS file
        self.m_size = 30 # the metadata Block size

        if(not os.path.isfile(self.FILE_SYSTEM)):
            self.__setup() # create the fileSystem if it doesn't exist

        self.systemFile = open(self.FILE_SYSTEM, "r") # open the systemFile in read+ mode
        self.systemFileContents =[line.strip() for line in self.systemFile]

        # the current size of the metadataBlock here
        self.current_size = int(self.systemFileContents[1].split("=")[1])

    def __del__(self):
        ''' The destructor of the Class'''
        self.systemFile.close()

    def __commitChanges(self): # commit the changes here
        with open(self.FILE_SYSTEM, "w") as file:
            file.writelines(map(lambda x:x+"\n", self.systemFileContents))

    def __setup(self):
        ''' Setup the File for the TextFS'''
        metadataBlock = "BLOCK: METADATA\n"
        storageBlock  = "BLOCK: STORAGE\n"

        #create the first metadataBlock
        lines = [metadataBlock, "current-size=0\n10 0\n", EOB, storageBlock]

        with open(self.FILE_SYSTEM, "w") as file:
            file.writelines(lines) # write all the lines in the file

    def __addMetadata(self, node):
        ''' Add the file related Metadata
            node = (filename, lineNo, size)'''

        adder = self.systemFileContents[2 + self.current_size].split(" ")

        # There is a slot available
        # add the node to the available slot
        adder.append("[" + str(node[0]) + "," + str(node[1]) + "," + str(node[2]) + "]")
        adder[1] = str(int(adder[1]) + 1) # increment the used slots

        self.systemFileContents[2 + self.current_size] = reduce(lambda x,y:x+" "+y, adder)

        if(int(adder[1]) == int(adder[0])):
            # all the slots of the line used
            self.systemFileContents[1] = "current-size=" + str(self.current_size + 1) # inc current-size

            # add a new line to write
            position = 2 + self.current_size + 1
            self.systemFileContents = self.systemFileContents[:position] + ["10 0"] + self.systemFileContents[position:]

            # increment all the first line numbers in previous metas
            for itr in range(2, position):
                line = self.systemFileContents[itr].split(" ")
                for jtr in range(2, len(line)):
                    details = line[jtr][1: len(line[jtr]) - 1].split(",")
                    node = "["+details[0]+","+str(int(details[1]) + 1)+","+details[2]+"]"
                    line[jtr] = node
                self.systemFileContents[itr] = reduce(lambda x,y:x+" "+y, line)

        # commit the changes to the actual file system
        self.__commitChanges()

    def __deleteMetadata(self, filename):
        ''' remove the Metadata of the deleted file
            filename = name of the file'''

        metas = []
        for itr in range(2, 2 + self.current_size + 1):
            metas = metas + self.systemFileContents[itr].split(" ")[2:]

        lastNode = False
        # delete the required meta
        for itr in range(0, len(metas)):
            fileNode = metas[itr]
            checker = fileNode[1:len(fileNode) - 1].split(",")
            if(checker[0] == filename):
                # file metadata node found
                if(itr == len(metas) - 1):
                    lastNode = True # case to be handled separately
                size = int(checker[2])
                metas.pop(itr) # file node deleted
                break

        if(not lastNode):
            # change the second field of every meta:
            # only if the deleted node is not the last node
            for jtr in range(itr, len(metas)):
                checker = metas[jtr][1:len(metas[jtr]) - 1].split(",")
                metas[jtr] = "[" + checker[0] +","+ str(int(checker[1]) - (size + 1)) +","+ checker[2] + "]"

        # restructure the nodes in the metadata block as follows

        if(len(metas) == (self.current_size * 10) - 1):
            # special case when a line has to be deleted completely
            # print "is this happening?"
            self.systemFileContents.pop(2 + self.current_size)
            self.current_size -= 1
            self.systemFileContents[1] = "current-size=" + str(self.current_size)

        for itr in range(2, 2 + self.current_size + 1):
            if(len(metas) >= 10):
                line = "10 10"
                for jtr in range(0, 10):
                    line = line + " " + metas.pop(0)
            else:
                blockLine = ""
                if(len(metas) != 0):
                    blockLine = reduce(lambda x,y:x+" "+y, metas)
                line = "10 " + str(len(metas)) + " " + blockLine

            self.systemFileContents[itr] = line

        # commit the changes the file system
        self.__commitChanges()

    def __searchFile(self, filename):
        systemFile = open(self.FILE_SYSTEM, "r") # open the systemFile in read+ mode
        self.systemFileContents =[line.strip() for line in systemFile]
        self.current_size = int(self.systemFileContents[1].split("=")[1])

        metas = []
        for itr in range(2, 2 + self.current_size + 1):
            metas = metas + self.systemFileContents[itr].split(" ")[2:]

        # This module is not concerned with the fact whether the file exists or not
        # That check has to be taken care off by the higher module
        # Thus the program will always reach the return statement in the following for loop
        for metafile in metas:
            checker = metafile[1:len(metafile)-1].split(",")
            if(checker[0] == filename):
                return (checker[1], checker[2])
    def setM_size(self, newSize):
        ''' Change the m_size'''
        self.m_size = newSize

    def addFile(self, filename, contents):
        ''' Adds the contents of the file to the FileStorageBlock
            filename = name of the file (String)
            contents = contents of the file ([lines])'''
        systemFile = open(self.FILE_SYSTEM, "r") # open the systemFile in read+ mode
        self.systemFileContents =[line.strip() for line in systemFile]

        start_point = len(self.systemFileContents) + 1
        size_of_file = len(contents)

        self.systemFileContents = self.systemFileContents + [SOF] + contents # add the file

        #commit the contents to the actual FILE_SYSTEM
        self.__commitChanges()

        # add the file related metadata
        self.__addMetadata((filename, start_point, size_of_file))

    def deleteFile(self, filename): # throws "File not found" exception
        ''' Removes a file from the FileSystem
            filename = name of the file to be removed (String)'''
        systemFile = open(self.FILE_SYSTEM, "r") # open the systemFile in read+ mode
        self.systemFileContents =[line.strip() for line in systemFile]
        self.current_size = int(self.systemFileContents[1].split("=")[1])

        start, size = map(int, self.__searchFile(filename))
        # delete the contents of the file
        self.systemFileContents = self.systemFileContents[0: start-1] + self.systemFileContents[(start + size):]

        #commit the changes to the actual FILE_SYSTEM
        self.__commitChanges()

        # Remove the entry of the file from the
        self.__deleteMetadata(filename)


    def readFile(self, start, size):
        ''' Retreives a file from the Storage block on the File System
            filename = name of the file to be removed (String)'''
        fileContents = [] # initialize an empty String
        linecache.clearcache() # clear the cache of the file
        for itr in range(int(start), int(start) + int(size) + 1):
            fileContents.append(linecache.getline(self.FILE_SYSTEM, itr).strip())
        return fileContents

Operator = FileOperator(".TextFS") # Object created for plug and play feature
# the name of the File System can be changed if required However it is not recommended to do so

# test script here
# Operator.addMetadata(("abc.txt", 69, 2))
# Operator.deleteMetadata("abc.txt")
# Operator.addFile("c.txt", ["I AM ANIMESH KARNEWAR", "I LOVE TO EAT FOOD", "IS THIS WORKING???"])
# Operator. deleteFile("jkl.txt")
# for line in Operator.readFile(9, 4):
#     print line
