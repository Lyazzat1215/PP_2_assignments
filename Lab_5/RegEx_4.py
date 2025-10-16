import re

def task_4(text):
    pattern=r'[A-Z][a-z]+'
    return re.findall(pattern, text)

test_text="Onerkhankyzy Lyazzat lzzt Programming PRINCIPLES Robotics aNd mechatronics"
result=task_4(test_text)
print("result:", result)