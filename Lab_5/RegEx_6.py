import re

def task_6(text):
    pattern=r'[ ,\.]'
    return re.sub(pattern, ':', text)

test_text = "Mlem, Mlem. friday Lzzt,onerkhan "
result=task_6(test_text)
print("Начальый:", test_text)
print("После замены:", result)