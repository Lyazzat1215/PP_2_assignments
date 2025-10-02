import math
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def show(self):
        print(f"Координаты точки: ({self.x}, {self.y})")
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    def dist(self, other_point):
        return math.sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)
# Тест
p1 = Point(1, 2)
p2 = Point(4, 6)
p1.show()
p2.show()
print("Расстояние между точками:", p1.dist(p2))
