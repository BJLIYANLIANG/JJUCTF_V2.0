import os
import time
import re
import subprocess
class Contain:
    def __init__(self):
        self.path = "./Container/" # jjuctf目录下的
    def startContain(self,containName):
        penv = dict(os.environ)
        cmd  = "docker-compose -f jjuctf/CTF_CONTAINER/"+containName[:-4]+"/docker-compose.yml up -d "
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, env=penv)
            return output
        except subprocess.CalledProcessError as e:
            time.sleep(15)
        raise Exception("failed to start docker-compose (called: %s): exit code: %d, output: %s" % (e.cmd, e.returncode, e.output))

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
        penv = dict(os.environ)
        for i in id:
            cmd = 'docker ps |grep ' + i[:12]
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, env=penv)
            output = str(result,encoding='utf-8')
            # print(output)
            # str123 = result
            pattern = re.compile(r'\d\.\d\.\d\.\d:\d*')
            a = pattern.search(output)
            b = a.group()[0]
            # print(b)
            url.append(b)
        return url

            # print(cmd)

        # print(a.readlines())
    def getDockerId(self,containName):
        cmd = "docker-compose -f jjuctf/CTF_CONTAINER/"+containName[:-4]+"/docker-compose.yml ps -q "
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

#pr
# print(b.stopContain('EasyPython'))
