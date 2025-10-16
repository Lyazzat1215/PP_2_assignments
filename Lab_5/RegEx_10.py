import re
def camel_to_snake(camel_str):
    pattern=r'([a-z])([A-Z])'
    snake_str=re.sub(pattern, r'\1_\2', camel_str)
    return snake_str.lower()

test_strings=["bakerStreet", "thePinkHouse", "dragonStone"]
for test in test_strings:
    result=camel_to_snake(test)
    print(f"'{test}' -> '{result}'")