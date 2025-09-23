#booleans 
# Bool represent only two value its: True or False
print(15 > 12) # true 
print(15 == 12) #false 
print(15 < 12) # false 
#так же можно делать через else-if, это уже определнные условия 
a = 15
b = 12
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a") 
  print(bool("Hello "))#ваще не пон прикола, если стринг то выведет true когда в строке что то есть, если ничего нет false 
print(bool(15==12))# тут уже numerical так что имеет какой то ответ, и если там 0 то выведет false
# whats return false 
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})
# дальше есть __bool__ и __len__, сначала идет проверке есть ли бул если его нет, то длину
class myclass():
  def __len__(self): #проверка длины 
    return 0 #тут 0 обьектов, будет false, но если бы было 4 то было бы true

myobj = myclass()
print(bool(myobj)) 
