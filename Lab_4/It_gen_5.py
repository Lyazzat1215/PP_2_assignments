def countdown(n):
    while n>=0:
        yield n
        n-=1
#try
for num in countdown(12):
    print(num)