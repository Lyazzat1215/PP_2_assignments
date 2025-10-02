class pp_2:
    def __init__(self):
        self.text = ""
    def getString(self, value):
        self.text = value
    def printString(self):
        print(self.text.upper())
# тест
s = pp_2()
s.getString("Lzzt")   # задаем строку
print(s.text)         # выводит как есть
s.printString()       # выводит большими буквами