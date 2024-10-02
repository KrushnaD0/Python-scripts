import os
import stat

def get_pids_using_file(file_path):
    pids = []
    # Get the inode of the file
    try:
        file_inode = os.stat(file_path).st_ino
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []
    except PermissionError:
        print(f"Permission denied to access '{file_path}'.")
        return []

    # Iterate through all running processes
    for pid in os.listdir('/proc'):
        if pid.isdigit():
            fd_dir = f'/proc/{pid}/fd'
            if os.path.exists(fd_dir):
                # Iterate through all file descriptors of the process
                for fd in os.listdir(fd_dir):
                    fd_path = os.path.join(fd_dir, fd)
                    try:
                        # Get the inode of the file descriptor
                        if os.stat(fd_path).st_ino == file_inode:
                            pids.append(pid)
                            break
                    except FileNotFoundError:
                        continue
                    except PermissionError:
                        continue
    return pids

def find_pids_by_pipe():
    pids = []

    for pid in os.listdir('/proc'):
        if pid.isdigit():
            fd_dir = f'/proc/{pid}/fd'
            if os.path.exists(fd_dir):
                # Iterate through all file descriptors of the process
                for fd in os.listdir(fd_dir):
                    fd_path = os.path.join(fd_dir, fd)
                    try:
                        if stat.S_ISFIFO(os.stat(fd_path).st_mode):
                            pids.append(pid)
                            break
                    except FileNotFoundError:
                        continue
                    except PermissionError:
                        continue
    return pids

def find_pids_by_pipe_inode(pipe_inode):
    pids = []

    for pid in os.listdir('/proc'):
        if pid.isdigit():
            fd_dir = f'/proc/{pid}/fd'
            if os.path.exists(fd_dir):
                # Iterate through all file descriptors of the process
                for fd in os.listdir(fd_dir):
                    fd_path = os.path.join(fd_dir, fd)
                    try:
                        if stat.S_ISFIFO(os.stat(fd_path).st_mode) and os.stat(fd_path).st_ino == pipe_inode:
                            print(os.stat(fd_path).st_mode)
                            pids.append(pid)
                            break
                    except FileNotFoundError:
                        continue
                    except PermissionError:
                        continue
    return pids


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Find PIDs using a specific file.")
    print("2. Find all PIDs with pipes.")
    print("3. Find PIDs using a specific pipe inode.")

    choice = input("Enter your choice (1, 2, or 3): ").strip()

    if choice == "1":
        file_path = input("Enter the file path: ").strip()
        if not file_path:
            print("File path cannot be empty.")
        else:
            pids = get_pids_using_file(file_path)
            if pids:
                print(f"Processes using {file_path}: {', '.join(pids)}")
            else:
                print(f"No processes are currently using {file_path}.")
    elif choice == "2":
        pids = find_pids_by_pipe()
        if pids:
            print(f"Processes using pipes: {', '.join(pids)}")
        else:
            print("No processes are currently using pipes.")
    elif choice == "3":
        pipe_inode_input = input("Enter the pipe inode: ").strip()
        if not pipe_inode_input.isdigit():
            print("Invalid inode. Inode should be a number.")
        else:
            pipe_inode = int(pipe_inode_input)
            pids = find_pids_by_pipe_inode(pipe_inode)
            if pids:
                print(f"Processes using pipe inode {pipe_inode}: {', '.join(pids)}")
            else:
                print(f"No processes are currently using pipe inode {pipe_inode}.")
    else:
        print("Invalid choice. Please select either 1, 2, or 3.")
