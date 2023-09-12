# FolderSynchronizer
## Description:
- Python program that synchronizes  two folders: Source and Replica. 
- The synchronization is **one-way**: after the synchronization, the content of the replica folder will be modified to exactly match content of the source folder.
- Synchronization is performed **periodically**, at an interval given by the user(in seconds)
- File creation/copying/removal operations **will be logged to a file** and to the **console output**.

## Usage:
#### ``` python sync_folders.py <source_path> <replica_path> <sync_interval_seconds> <log_file_path> ```
- it may be needed to provide the full path of the python executable
- the provided time MUST be in seconds
- the log file will be created ate the specified path if it does not exist

  ### The provided folders and log file are for testing purpose. The code works with any given folders and files
