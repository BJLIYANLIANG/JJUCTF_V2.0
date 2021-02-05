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
        penv = dict(os.environ)
        cmd = "docker-compose -f jjuctf/CTF_CONTAINER/"+containName[:-4]+"/docker-compose.yml stop"
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, env=penv)
            return output
        except subprocess.CalledProcessError as e:
            time.sleep(15)
        raise Exception("failed to start docker-compose (called: %s): exit code: %d, output: %s" % (e.cmd, e.returncode, e.output))


    def stopContainByDockerID(self,dockerID):
        penv = dict(os.environ)
        cmd = "docker stop "+dockerID
        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, env=penv)
            return 1
        except subprocess.CalledProcessError as e:
            time.sleep(5)

    def dockerBuild(self):
        penv = dict(os.environ)
        cmd = ""
        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, env=penv)
            return 1
        except subprocess.CalledProcessError as e:
            time.sleep(5)


    def geturl(self,id):
        #  得到ip和端口
        #  [['0.0.0.0', '5000']]
        for i in id:
            cmd = 'docker ps |grep ' + i[:12]
            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
            p.wait()
            out = p.stdout.read()
            print(out)
            re_result = re.search(r'\d\.\d\.\d\.\d\:\d*',str(out))
            return re_result.group()


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