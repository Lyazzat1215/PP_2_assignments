import os

def safe_delete_file(filepath):
    if not os.path.exists(filepath):
        print(f"File '{filepath}' does not exist")
        return
    
    if not os.access(filepath, os.W_OK):
        print(f"No write access to '{filepath}'")
        return
    
    try:
        os.remove(filepath)
        print(f"File '{filepath}' deleted successfully")
    except Exception as e:
        print(f"Error deleting file: {e}")

with open('test_delete.txt', 'w') as f:
    f.write("This file will be deleted")

safe_delete_file('test_delete.txt')