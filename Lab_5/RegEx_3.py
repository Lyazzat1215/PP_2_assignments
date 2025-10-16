import re

def task_3(text):
    pattern=r'[a-z]+_[a-z]+'
    return re.findall(pattern, text)

test_text="Onerkhankyzy_Lyazzat lzzt_onrkhn programming_principles ROBOTICS_MECHATRONICS"
result=task_3(test_text)
print("Rезультат:", result)