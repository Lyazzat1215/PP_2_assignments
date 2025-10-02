class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    def area(self):
        return self.length * self.width
# Тест
rectangle = Rectangle(4, 6)
print("Площадь Rectangle:", rectangle.area())
