import re

def task_1(text):
    pattern=r'ab*'
    return "match" if re.search(pattern, text) else "no match"

test_strings=["a", "ab", "abb", "ac", "b", "abc"]
for test in test_strings:
    print(f"'{test}': {task_1(test)}")
print()