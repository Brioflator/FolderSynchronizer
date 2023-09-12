import os
import sys
import shutil
import time
import threading

# Global variable to signal the synchronization loop to stop
stop_sync = False


def sync_folders(source_path, replica_path, log_file_path, sync_interval):
    global stop_sync

    while not stop_sync:
        try:
            # List files in both source and replica folders
            # os.listdir() returns a list of all files in a folder
            # it is converted to a set to make it easier to calculate and to avoid duplicates (safety measure)
            # set items are unchangeable, so file names cannot be modified/corrupted
            source_files = set(os.listdir(source_path))
            replica_files = set(os.listdir(replica_path))

            # Calculate files to create, copy and files to delete in replica folder
            # we are using set operations to calculate the difference between the two sets
            # files that exist in source but not in replica
            files_to_create = source_files - replica_files
            # files that exist in replica but not in source
            files_to_delete = replica_files - source_files
            files_to_copy = {
                file for file in files_to_create if "copy" in file or "Copy" in file}  # files that are copied and pasted in source

            # Create missing files from source to replica
            # shutil.copy2() copies a file from source to destination
            for file_to_create in files_to_create:
                # get the path of the file to be synced
                source_file_path = os.path.join(source_path, file_to_create)
                # create the path of the file to be created
                replica_file_path = os.path.join(replica_path, file_to_create)
                # copy the file from source to replica
                shutil.copy2(source_file_path, replica_file_path)

                if file_to_create in files_to_copy:  # if the file is a copy, log it as a copy
                    log_operation("COPY", source_file_path,
                                  replica_file_path, log_file_path)
                else:  # if the file is not a copy, log it as a create
                    log_operation("CREATE", source_file_path,
                                  replica_file_path, log_file_path)

            # Delete extra files in replica
            for file_to_delete in files_to_delete:
                # get the path of the file to be deleted
                replica_file_path = os.path.join(replica_path, file_to_delete)
                os.remove(replica_file_path)  # delete the file
                log_operation("DELETE", "", replica_file_path,
                              log_file_path)  # log the deletion

            print("Folders are synced.")

        except Exception as e:  # if an error occurs, log it and continue
            print(f"Error during synchronization: {str(e)}")

        # wait for the specified interval before syncing again
        time.sleep(sync_interval)


def log_operation(operation, source_file, replica_file, log_file_path):
    # create the log entry
    log_entry = f"[{operation}] {source_file} -> {replica_file}\n"
    # open the log file in append mode and write the log entry
    with open(log_file_path, "a") as log_file:
        log_file.write(log_entry)
    print(log_entry, end="")  # print the log entry to the console


def main():
    if len(sys.argv) != 5:  # if the call is missing arguments, print usage and exit
        print("Usage: python sync_folders.py <source_path> <replica_path> <sync_interval_seconds> <log_file_path>")
        sys.exit(1)

    # get the arguments from the command line
    source_path = sys.argv[1]
    replica_path = sys.argv[2]
    sync_interval = int(sys.argv[3])
    log_file_path = sys.argv[4]

    # Check if source and replica folders exist
    if not os.path.exists(source_path) or not os.path.exists(replica_path):
        print("Source and replica folders must exist.")
        sys.exit(1)

    print("------------------------------------------------------------------------------------------------------------------\n")
    print(
        f"Syncing {source_path} to {replica_path} every {sync_interval} seconds. Logging to {log_file_path}")
    print("\n\n------------------------------------------------------------------------------------------------------------------")

    # By using threads, we can check for user input to exit the program while the synchronization is running
    # This way, the keyboard interrurpt will not interfere with the sync function

    # Start the synchronization thread
    sync_thread = threading.Thread(target=sync_folders, args=(
        source_path, replica_path, log_file_path, sync_interval))  # create a thread that will run the sync_folders function
    sync_thread.start()

    # Wait for user input to exit
    try:
        # The program will be paused at this point until the user interacts
        input("PRESS ENTER TO EXIT...\n")
    except KeyboardInterrupt:
        pass  # if the user presses CTRL+C, ignore the exception and continue

    # Set the global flag to stop synchronization
    global stop_sync
    stop_sync = True

    # Wait for the sync thread to finish
    sync_thread.join()
    print("PROGRAM EXITING.")
    print("##################################################################################################################\n")


if __name__ == "__main__":
    main()


# usage: python sync_folders.py <source_path> <replica_path> <sync_interval_seconds> <log_file_path>
# it may be needed to provide the full path of the python executable
# the provided time MUST be in seconds
# the log file will be created ate the specified path if it does not exist
