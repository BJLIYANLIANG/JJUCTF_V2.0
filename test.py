from jjuctf.Contain import *
b = Contain()
# # b.startContain("EasyPython")
# c = b.stopContain('EasyPython')
# print(c)
id = b.getDockerId("EasyPython.zip")
print(b.geturl(id))