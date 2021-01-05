import datetime
str = "2021-01-22 20:24:01"
dd = datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
print(dd)

