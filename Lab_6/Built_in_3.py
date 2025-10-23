def palindrome(text):
    cleaned_text=''.join(char.lower() for char in text if char.isalnum())
    return cleaned_text==cleaned_text[::-1]

test_string="А роза упала на лапу Азора"
print(f" Текст'{test_string}' палиндром? {palindrome(test_string)}")