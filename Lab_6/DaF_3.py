import os

def analyze_path(path):
    if os.path.exists(path):
        print(f"Path exists: {path}")
        
        if os.path.isfile(path):
            directory=os.path.dirname(path)
            filename=os.path.basename(path)
            print(f"Directory: {directory}")
            print(f"Filename: {filename}")
        else:
            print("This is a directory")
    else:
        print("Path does not exist")

analyze_path(__file__) 