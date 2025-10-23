def check_tuple(elements):
    return all(elements)

tuple1=(True, True, True)
tuple2=(True, False, True)

print(f"All elements of {tuple1} are True: {check_tuple(tuple1)}")
print(f"All elements of {tuple2} are True: {check_tuple(tuple2)}")