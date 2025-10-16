import re
def insert_spaces(text):
    pattern =r'(?<=[a-z])(?=[A-Z])'
    return re.sub(pattern, ' ', text)

test_strings=["LzztOnerkhan", "RoboticsMechatronics", "ProgrammingPrinciples"]
for test in test_strings:
    result=insert_spaces(test)
    print(f"'{test}' -> '{result}'")