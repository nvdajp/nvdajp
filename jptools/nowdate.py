from datetime import datetime as dt

print(dt.now().strftime("%y%m%d") + chr(dt.now().hour + 97))
