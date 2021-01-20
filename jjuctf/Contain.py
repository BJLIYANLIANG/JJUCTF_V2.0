import os
import docker
import re
class Contain:
    def __init__(self):
        self.path = "./Container/" # jjuctf目录下的

    def startContain(self,containName):
        cmd  = "docker-compose -f jjuctf/CTF_CONTAINER/"+containName[:-4]+"/docker-compose.yml up -d "
        startdocker = os.popen(cmd)
        if str(startdocker.readlines()).find('Errno'):
            return 0



    def stopContain(self,containName):
        cmd = "docker-compose -f jjuctf/CTF_CONTAINER/"+containName[:-4]+"/docker-compose.yml stop"
        # print(cmd)
        try:
            result = os.system(cmd)
            # print(a.readlines())
            if result != 0:
                return 0
            else:
                return 1
        except:
            return 0


    #  得到ip和端口
    #  [['0.0.0.0', '5000']]
    def geturl(self,id):
        url = []
        for i in id:
            cmd = 'docker ps |grep ' + i[:12]
            result = os.popen(cmd)
            str123 = str(result.readlines())
            pattern = re.compile(r'\d\.\d\.\d\.\d:\d*->\d*')
            a = pattern.search(str123)
            b = a.group()
            c = b.replace('[','').replace(']','').split(':')
            d = c[1].split('->')
            # print(d)
            i = []
            i.append(c[0])
            i.append(d[1])
            url.append(i)
        return url


            # print(cmd)

        # print(a.readlines())
    def getDockerId(self,containName):
        cmd = "docker-compose -f jjuctf/CTF_CONTAINER/"+containName[:-4]+"/docker-compose.yml ps -q"
        result  = os.popen(cmd)
        if result:
            id = []
            for i in result:
                id.append(i.replace('\n',''))
            return id
        else:
            return []
        # print(a.readlines())


#
# b = Contain()
# # b.startContain("EasyPython")
# c = b.stopContain('EasyPython')
# print(c)
# print(b.geturl("EasyPython"))
#pr
# print(b.stopContain('EasyPython'))
