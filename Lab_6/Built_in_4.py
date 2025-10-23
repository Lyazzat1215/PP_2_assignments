import math
import time

def sqrt_after_ms(number, milliseconds):
    time.sleep(milliseconds / 1000)
    result=math.sqrt(number)
    return result

number=25100
delay=2123
result=sqrt_after_ms(number, delay)
print(f"Square root of {number} after {delay} milliseconds is {result}")