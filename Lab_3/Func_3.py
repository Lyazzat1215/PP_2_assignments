def solve(numheads, numlegs):

    for rabbits in range(numheads + 1):
        chickens = numheads - rabbits
        if 4 * rabbits + 2 * chickens == numlegs:
            return rabbits, chickens
    return "Нет решения"
# Тест
result = solve(35, 94)
print(f"Кроликов: {result[0]}, Кур: {result[1]}")