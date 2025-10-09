def divisible_by_3_and_4(n):
    for i in range(0,n+1):
        if i%3==0 and i%4==0:
            yield i
def generate_divisible_numbers(n):
    return divisible_by_3_and_4(n)

n=120
for num in generate_divisible_numbers(n):
    print(num)