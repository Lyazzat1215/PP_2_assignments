import re

def split_at_uppercase(text):
    pattern=r'[A-Z][^A-Z]*'
    return re.findall(pattern, text)

test_strings=["OnerkhanLyazzat", "PythonRegex", "MlemMlem", "OneTwoThree"]
for test in test_strings:
    result=split_at_uppercase(test)
    print(f"'{test}' -> {result}")