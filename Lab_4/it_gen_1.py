def squares_up_to_n(N):
    for i in range(1,N+1):
        yield i**2
N=8
for square in squares_up_to_n(N):
    print(square)