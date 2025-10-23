import os

def check_path_access(path):
    print(f"Checking access for: {path}")
    print(f"Exists: {os.path.exists(path)}")
    
    if os.path.exists(path):
        print(f"Readable: {os.access(path, os.R_OK)}")
        print(f"Writable: {os.access(path, os.W_OK)}")
        print(f"Executable: {os.access(path, os.X_OK)}")

check_path_access(".")