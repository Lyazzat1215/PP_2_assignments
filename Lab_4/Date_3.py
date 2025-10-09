from datetime import datetime
current_datetime=datetime.now()
datetime_without_microseconds=current_datetime.replace(microsecond=0)

print("Original:", current_datetime)
print("Without microseconds:", datetime_without_microseconds)