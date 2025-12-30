import os
import crypt
import sys
import argparse
import shutil

# --- Configuration ---
HOST_DATA_DIR = "../data"
HOST_PASSWD_FILE = "../config/ftpd.passwd"
CONTAINER_HOME_ROOT = "/home/ftp"

# Start assigning IDs from this number
START_UID = 1001
GID = 1000

def get_next_uid():
    if not os.path.exists(HOST_PASSWD_FILE): return START_UID
    max_uid = START_UID - 1
    with open(HOST_PASSWD_FILE, "r") as f:
        for line in f:
            try:
                parts = line.strip().split(':')
                if len(parts) >= 3:
                    uid = int(parts[2])
                    if uid > max_uid: max_uid = uid
            except ValueError: continue
    return max_uid + 1

def get_hash(password):
    return crypt.crypt(password, crypt.mksalt(crypt.METHOD_MD5))

def add_user(username, password):
    # Host Paths
    host_user_home = os.path.join(HOST_DATA_DIR, username)
    public_dir = os.path.join(host_user_home, "Public")
    private_dir = os.path.join(host_user_home, "Private")
    
    # Docker Path (CRITICAL FIX: Point to the user's subfolder, not the root)
    docker_user_home = os.path.join(CONTAINER_HOME_ROOT, username)

    if os.path.exists(HOST_PASSWD_FILE):
        with open(HOST_PASSWD_FILE, "r") as f:
            if any(line.startswith(f"{username}:") for line in f):
                print(f"Error: User '{username}' already exists.")
                return

    # Generate ID and Write Entry
    new_uid = get_next_uid()
    password_hash = get_hash(password)
    
    # We point them to docker_user_home (/home/ftp/username) so ownership matches
    entry = f"{username}:{password_hash}:{new_uid}:{GID}::{docker_user_home}:/bin/false\n"

    with open(HOST_PASSWD_FILE, "a") as f:
        f.write(entry)

    # Create Directories
    try:
        os.makedirs(public_dir, exist_ok=True)
        os.makedirs(private_dir, exist_ok=True)
        
        # Set Ownership
        os.chown(host_user_home, new_uid, GID)
        os.chown(public_dir, new_uid, GID)
        os.chown(private_dir, new_uid, GID)

        # Set Permissions
        os.chmod(host_user_home, 0o755)
        os.chmod(public_dir, 0o777)
        os.chmod(private_dir, 0o700)
    except Exception as e:
        print(f"Error creating directories: {e}")
        return

    print_success(username, password, new_uid)

def delete_user(username):
    if not os.path.exists(HOST_PASSWD_FILE): return
    lines = []
    found = False
    with open(HOST_PASSWD_FILE, "r") as f:
        for line in f:
            if line.startswith(f"{username}:"):
                found = True
            else:
                lines.append(line)
    if found:
        with open(HOST_PASSWD_FILE, "w") as f:
            f.writelines(lines)
        print(f"User '{username}' removed.")
    else:
        print(f"Error: User '{username}' not found.")

def print_success(username, password, uid):
    print("success")
    print(f"user name : {username}")
    print(f"password : {password}")
    print(f"System ID : {uid}")

if __name__ == "__main__":
    if not os.path.exists(HOST_PASSWD_FILE):
        open(HOST_PASSWD_FILE, 'a').close()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    p_add = subparsers.add_parser("add")
    p_add.add_argument("username")
    p_add.add_argument("password")
    p_del = subparsers.add_parser("del")
    p_del.add_argument("username")
    args = parser.parse_args()
    if args.command == "add": add_user(args.username, args.password)
    elif args.command == "del": delete_user(args.username)
