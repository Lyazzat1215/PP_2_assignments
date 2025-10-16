import re

def snake_to_camel(snake_str):
    pattern=r'_([a-z])'
    return re.sub(pattern, lambda x: x.group(1).upper(), snake_str)

test_strings=["Lyazzat_Onerkhan", "mlem_mlem", "Reg_Ex"]
for test in test_strings:
    result=snake_to_camel(test)
    print(f" '{result}' (regex)")