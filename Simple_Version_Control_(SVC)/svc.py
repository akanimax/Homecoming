#!/usr/bin/python

''' This is the main integrated python script that runs the svc application '''
# coded by botMan

import sys # required to handle the command line arguments
import re # regular expression library
import os # standard operating system library
from MetadataOperator import Operator as MO # module providing the builtin functionality

usageOfTool = ("\nSorry Wrong Usage of the tool. Use the following formats: " +
              "\n\t1.) To commit changes to the file : svc <filename.txt>"   +
              "\t2.) To view a particular version    : svc <filename.txt> <version No.>\n")

noOfArguments = len(sys.argv) # the number of command line arguments

if(noOfArguments < 2 or noOfArguments > 3):
    print usageOfTool
    exit()

pattern_commit = ".txt" # regex pattern for the commit operation
pattern_readversion = "^-?[0-9]+$" # regex pattern for the read version operation

if(noOfArguments == 2):
    argument = sys.argv[len(sys.argv) - 1]

    if(re.search(pattern_commit, argument)):
        # "\n\nthis is where we handle the commit file part\n"
        filename = argument # The argument is actually the filename

        # check if the file exists or not
        if(not os.path.isfile(argument)):
            print "\nSorry the FILE doesn't exist\n"
            exit()
        # If the file exists: simply call the module that takes care of the commit part
        MO.commit(filename)

elif(noOfArguments == 3):
    argument1 = sys.argv[len(sys.argv)-2]
    argument2 = sys.argv[len(sys.argv)-1]

    if(re.search(pattern_commit, argument1) and re.search(pattern_readversion, argument2)):
        # "\n\nthis is where we handle the retrieve a version part\n"

        filename = argument1
        versionNumber = argument2

        # call the module that takes care of the read Version part
        contents = MO.retrieve(argument1, argument2)
        if contents != None:
            print "\nContents of the Version ", argument2, " are:\n"
            for line in contents:
                print line
            print "\n\n"

    else:
        print usageOfTool

else:
    print usageOfTool
