import shutil

def copy_file(source, destination):
    shutil.copy2(source, destination)
    print(f"File copied from {source} to {destination}")

with open('source.txt', 'w') as f:
    f.write("Hello, World!\nThis is a test file.")

copy_file('source.txt', 'destination.txt')