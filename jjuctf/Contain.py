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

    def docker_start_by_imagesID(self,group_name,images_id,ip):
        penv = dict(os.environ)
        cmd = 'docker run --name %s  --network awd --ip %s  -d  %s'%(group_name,ip,images_id)
        # print(cmd)
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, env=penv)
            return str(result)[2:14]

        except subprocess.CalledProcessError as e:
            time.sleep(1)

    # def docker_gen_dockerIP(self,):
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
    # 为容器添加flag
    def insert_awd_flag(self,image_id,flag,file_path):
        penv = dict(os.environ)
        cmd = "docker exec -u root %s bash -c 'echo '%s' > %s'"%(image_id,flag,file_path)
        # print(cmd)
        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, env=penv)
            return 1
        except subprocess.CalledProcessError as e:
            print(e.output)
            return -1
    def check_awd_status(self,images):
        pass

# docker = Contain()
# a = docker.insert_awd_flag('ef49418c0de4234','flag{test}','/flag')
# print(a)
