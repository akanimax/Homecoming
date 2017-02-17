#!/usr/bin/python
'''A text based File System for simple storage and retreival of the text based files'''

# coded by botMan

from FileSystemMounter import Mounter # the FileSystemMounter module for the FileSystem
import os # the standard operating system library

# define the usege string to displayed on helps
usage = ("\nUse the following commands:" +
         "\n\t1) create <filename> <external file path>" +
         "\n\t2) echo <filenane>" +
         "\n\t3) delete <filename>" +
         "\n\t4) ls" +
         "\n\t5) help" +
         "\n\t6) exit\n")

command_not_found = "\nCommand Not found!\ntype help to check the usage of the tool\n"

# print the initial Welcome message
print "==== Welcome to the Secret TextFS fileSystem ====\n\n"
Mounter.mount() # mount the fileSystem

done = False # create a done flag
# start the REPL interpreter below
while not done:
    command = raw_input(">>>> ") # input the command from the user:
    command_inter = command.split(" ") # the command interpretation

    if(len(command_inter) == 1):
        # case when the command could be ls, help or exit

        if(command_inter[0] == "ls"):
            # handle ls command
            print "\nCurrent Files in the FileSystem:"
            for line in enumerate(Mounter.listFiles()): # retrieve a list of all files from the Mounter object
                print int(line[0])+1,") ",line[1]
            print "\n" # print extra newline

        elif(command_inter[0] == "help"):
            # the help command fired
            print usage

        elif(command_inter[0] == "exit"):
            # handle the exit command
            print "Have a nice Day! and Keep away from Mr. Suresh!\n"
            done = True # simply change the done flag

        else:
            if(command_inter[0] == ""):
                print "\n"
            else:
                # command not found case
                print command_not_found

    elif(len(command_inter) == 2):
        # case for the echo and the delete command

        if(command_inter[0] == "echo"):
            # echo command entered by the user
            filename = command_inter[1] # record the entered filename
            try:
                contents = Mounter.readFile(filename) # you can get a file not found exception here
                # print the file contents
                print "\nThe Contents of the file:"
                for line in contents:
                    print line
                print "\n" # print extra newline for structured output
            except Exception as exc:
                print exc

        elif(command_inter[0] == "delete"):
            # delete command entered by the user
            filename = command_inter[1]
            try:
                Mounter.deleteFile(filename)
                print "\nFile deleted Successfully\n"
            except Exception as exc:
                print exc # Exception message

        else:
            # command not found case:
            print command_not_found

    elif(len(command_inter) == 3):
        # create file case
        file_orginal = command_inter[2]
        file_to_be_created = command_inter[1]

        if(not os.path.isfile(file_orginal)):
            print "\nERROR: FILE TO CREATED NOT FOUND!\n"
        else:
            contents = [line.strip() for line in open(file_orginal, "r").readlines()]
            try:
                Mounter.addFile(file_to_be_created, contents) # this may throw exception
                print "\nFile Added Successfully\n" # acknowledgement message
            except Exception as exc:
                print exc
    else:
        # some very odd command not found case:
        print command_not_found
