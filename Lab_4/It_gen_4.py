def squares(a, b):
    for i in range(a, b+1):
        yield i**2
# Тест
a, b = 1, 10
for sq in squares(a, b):
    print(sq)