# Homecoming
repository for mini-projects


### SVC
Title: Simple Version Control (SVC) application<br>
Run command: <br>
1) $python svc.py \<filename\> //To commit <br>
2) $python svc.py \<filename\> \<version_No\> //To View a particular Version <br>
<br>
#####Description:<br>
The application maintains efficient logs in the logfile created for any text file that is to be tracked under the svc. Inside the log file strategic checkpoints are created to retrieve the particular version contents efficiently.<br>
<br>
Features:<br>
1) Only single line modifications are allowed.<br>
2) No limit on no. of characters and no. of lines.<br>
3) The application works with multiple files hence the retrieval command requires filename and version number.<br>
4) Single line replace of text is also allowed (Though it means two modifications deletion and addition).<br>
5) Fast line based retrieval of data from the file.<br>
<br><br>


### FSS
Title:File System Simulator <br>
Run command: <br>
1) $python TextFS.py //To start the command interpreter <br>
2) >>>>help //To view all the commands <br>
<br>
#####Description:<br>
This application maintains a single hidden log file that contains all the metadata for the inserted files and the actual data in the FileSystem. The application is intended to provide the requirements for the scenarios mentioned in Mr. Ramesh's case.<br>
<br>
Features:<br>
1) Simple format of file storage in the fileSystem.<br>
*2) Functionality of a lookaside buffer for fast retreival of files while reading is integrated in the application.<br>
3) Modularity of code is maintained.<br>
4) Searching of files is in constant time because metadata is mounted in a hashmap in main memory. <br>
<br><br>
