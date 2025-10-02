def fahrenheit_to_celsius(fahrenheit):
    return (5 / 9) * (fahrenheit - 32)
# Тест
def main():
    f_temp = 63
    c_temp = fahrenheit_to_celsius(f_temp)
    print(f"{f_temp}°F = {c_temp:.2f}°C")
# Вызов функции
if __name__ == "__main__":
    main()