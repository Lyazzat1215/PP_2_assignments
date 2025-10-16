import re
def task_2(text):
    pattern=r'ab{2,3}'
    return "match" if re.search(pattern, text) else "no match"

test_strings=["a", "ab", "abb", "abbb", "abbbb", "ac"]
for test in test_strings:
    print(f"'{test}': {task_2(test)}")
print()