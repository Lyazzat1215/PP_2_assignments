import re
def task_5(text):
    pattern=r'a.*b$'
    return "match" if re.search(pattern, text) else "no match"

test_strings=["acb", "a123b", "ab", "a b", "ba", "abc"]
for test in test_strings:
    print(f"'{test}': {task_5(test)}")
print()