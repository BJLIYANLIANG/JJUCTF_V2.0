import hashlib
a = hashlib.md5('905008'.encode('utf-8'))
print(a.hexdigest())