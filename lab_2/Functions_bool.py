# boolean functions
def myFunction() : # функция в true
  return 20
print(myFunction())#поч это бул хз, просто как принт, ради булла надо еще
print(bool(myFunction()))# тут уже проверка булла
# if-else ofc
def myFunction() :
  return True
if myFunction():
  print("YES!")
else:
  print("NO!")
# isinstanse уже интереснееБ оно проверяет тип обьекта или переменнной   
x = 200 # это int, так что выведет true 
print(isinstance(x, int))
