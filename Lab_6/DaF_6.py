def generate_alphabet_files():
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        filename=f"{letter}.txt"
        with open(filename, 'w') as file:
            file.write(f"This is file {filename}\n")
        print(f"Created: {filename}")

generate_alphabet_files()