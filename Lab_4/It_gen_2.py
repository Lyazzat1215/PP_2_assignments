def even_numbers(n):
    for i in range(0,n+1,2):
        yield i
n=int(input("Числа: "))
result = [str(x) for x in even_numbers(n)]
print(", ".join(result))