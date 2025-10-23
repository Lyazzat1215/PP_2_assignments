def write_list_to_file(data_list, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for item in data_list:
            file.write(str(item)+'\n')
    print(f"List written to {filename}")

my_list = ["Apple", "Banana", "Cherry", 123, 45.67]
write_list_to_file(my_list, 'output.txt')