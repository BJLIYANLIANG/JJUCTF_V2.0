import os
import docker

class Contain:
    def __init__(self):
        self.path = "./Container/" # jjuctf目录下的


    def startContain(self,ContainName):
        # pass
        # 等学一下docker库后再实现功能
        port = range(54000,54332)

        cmd  = "cd "+self.path+ContainName+";docker-compose up -d "
        # path = self.path+ContainPath
        # print(path)
        print(cmd)
        a = os.popen(cmd)
        print(a.readlines())
    def stopContain(self):
        pass



#
b = Contain()
b.startContain("EasyPython")

