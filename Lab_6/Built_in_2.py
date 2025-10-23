def count_case_letters(text):
    upper_count=sum(1 for char in text if char.isupper())
    lower_count=sum(1 for char in text if char.islower())
    return upper_count, lower_count

text="Onerkhan Lyazzat,RoBotics And Mechatronics "
upper, lower=count_case_letters(text)
print(f"Коичество заглавных букв: {upper}")
print(f"Количество строчных букв: {lower}")