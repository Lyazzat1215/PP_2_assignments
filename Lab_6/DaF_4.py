def count_file_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            line_count=sum(1 for line in file)
        return line_count
    except FileNotFoundError:
        return "File not found"

with open('sample.txt', 'w') as f:
    f.write("Line 1\nLine 2\nLine 3\n")

print(f"Number of lines: {count_file_lines('sample.txt')}")