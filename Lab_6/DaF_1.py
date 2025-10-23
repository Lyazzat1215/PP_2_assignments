import os

def list_directory_contents(path="."):
    print("Directories:")
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            print(f"  {item}")
    
    print("\nFiles:")
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            print(f"  {item}")
    
    print("\nAll items:")
    for item in os.listdir(path):
        print(f"  {item}")

list_directory_contents()