#!usr/bin/python

''' This is the module that will take care of the metada related operations
    for the svc version control operations '''

# coded by botMan

import os # os library
import linecache # module for fast file operations based on lines

class MetadataOperator(object):
    ''' The MetadataOperator class for actual version control'''

    def __getLastContents(self, filename):
        metadata_fileName = ".svc_" + filename # filename for the metadata maintainer
        metadata = open(metadata_fileName, "r") # open file in w+ mode create if not present

        numOfVersions = sum(1 for line in metadata)
        metadata.close()

        return self.retrieve(filename, numOfVersions - 1) # get the contents of the latest version

    def __init__(self):
        ''' Constructor For the Class
            Default value for checkpoint factor is 10'''
        self.CHECKPOINT_FACTOR = 5 # current default checkpoint value in the metadata maintainer

    def setCheckpointFactor(self, newFactor):
        '''
            Function to set the CHECKPOINT_FACTOR explicitly
        '''
        self.CHECKPOINT_FACTOR = newFactor

    def commit(self, filename):
        ''' The code for commit operation comes here '''
        operableFile = open(filename, "r")
        currentContents = [line.strip() for line in operableFile] # get the current contents of the file

        metadata_fileName = ".svc_" + filename # filename for the metadata maintainer
        metadata = open(metadata_fileName, "a+") # open file in w+ mode create if not present

        numOfVersions = sum(1 for line in metadata)

        # Check if the changes are single line or not
        lastContents = self.__getLastContents(filename)

        if(lastContents == None):
            # First time commit case
            lastContents = [] # initialize an empty list for last contents
            lenLastContents = 0
        else:
            lenLastContents = len(lastContents)

        if(len(currentContents) < lenLastContents):
            if((len(currentContents) + 1) == lenLastContents):
                #case of last line deletion handled separately
                metadata.write(str(numOfVersions) + "%%%%" + str(lenLastContents) + "%%%%" +
                "-\n")
            else:
                print "\nSorry, There are more than single line changes in the FILE\n"
                return None

        else:
            for itr in range(lenLastContents, len(currentContents)):
                lastContents.append("")

            # hidden statements for the testing purpose
            # print currentContents
            # print lastContents

            #Check again if there are more than single line changes in the file:
            changes = 0
            ptr = -1
            for itr in range(0, len(lastContents)):
                if(lastContents[itr] != currentContents[itr]):
                    changes += 1
                    ptr = itr

            if(changes == 0):
                print "\nSorry, The file hasn't changed\n"
                return None

            elif(changes > 1):
                print "\nSorry, There are more than single line changes in the FILE\n"
                return None

            else:
                if((numOfVersions % self.CHECKPOINT_FACTOR) == 0):
                    # Checkpoint case Store all the Data in the MetadataFile
                    metadata.write(str(numOfVersions) + "%%%%" +
                        reduce(lambda x, y: x + "%%%%" + y, currentContents) + "\n")
                else:
                    # non checkpoint case
                    if(currentContents[ptr] == ""):
                        # case of single line deletion
                        metadata.write(str(numOfVersions) + "%%%%" + str(ptr + 1) + "%%%%" +
                        "-\n")
                    else:
                        # case of addition of new_Line
                        metadata.write(str(numOfVersions) + "%%%%" + str(ptr + 1) + "%%%%" +
                        "+" + "%%%%" + currentContents[ptr] + "\n")

        operableFile.close()
        metadata.close()
        print "\n***COMMIT SUCCESSFUL***\n"

    def retrieve(self, filename, version):
        '''The function returns the contents at a particular version number'''
        version = int(version) # cast the version number to intger if it may not be and integer

        metadata_fileName = ".svc_" + filename # filename for the metadata maintainer
        metadata = open(metadata_fileName, "r") # open file in w+ mode create if not present

        numOfVersions = sum(1 for line in metadata)

        metadata.close()

        #handle the excess version number case
        if(version >= numOfVersions):
            print "No such version exists"
            return None

        elif(version < 0):
            return None

        else:
            # start from the nearest checkpoint and keep updating the
            # appropriate lines in the contents

            lastCheckpoint = version - (int(version) % int(self.CHECKPOINT_FACTOR))
            contents = linecache.getline(metadata_fileName, (lastCheckpoint + 1)).strip().split("%%%%")[1:]

            for itr in range((lastCheckpoint + 2), (version + 2)):
                operation = linecache.getline(metadata_fileName, itr).strip().split("%%%%")

                if(operation[2] == '+'):
                    if(int(operation[1]) <= len(contents)):
                        contents[int(operation[1]) - 1] = operation[3]
                    else:
                        for jtr in range(len(contents), int(operation[1])- 1):
                            contents.append("")
                        contents.append(operation[3])

                elif(operation[2] == '-'):
                    contents[int(operation[1])-1] = ""

            return contents # return the contents of the particular version

Operator = MetadataOperator() # object already created for plug and play feature
# Operator.commit("file1.txt")
# Operator.retrieve("file1.txt", 3)
