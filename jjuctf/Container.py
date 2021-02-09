import os
import time
import re
import subprocess

class Contain:
    def __init__(self):
        self.path = "./Container/" # jjuctf目录下的

    # Function to execute any command
    def cmd_exec(self,exec_loc, cmd, remote_ip=" "):
        if exec_loc == 1:
            output = subprocess.run(["ssh", "root@{r}".format(r=remote_ip), cmd],
                                    shell=False,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, check=True)
        else:
            output = subprocess.run(cmd,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, check=True)

        result = output.stdout
        if (result == "b\'\'"):
            error = output.stderr
            print("Error: {e}".format(e=error.decode('utf-8')))
        else:
            print(result.decode('utf-8'))
        # print()

    # Function to stop docker container
    def docker_con_stop(self,exec_loc, docker_container_id, remote_ip):
        cmd = "docker stop " + docker_container_id
        a = self.cmd_exec(exec_loc, cmd, remote_ip)
        print(a)


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
            return -1

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

    def docker_add_user(self,container_id,user,passwd):
        # 生成密码
        penv = dict(os.environ)
        create_user_cmd = 'docker exec -u root %s useradd -m %s'%(container_id,user)
        add_passwd_status = subprocess.call(create_user_cmd, stderr=subprocess.STDOUT, shell=True, env=penv)
        # print(type(add_passwd_status),add_passwd_status)
        if add_passwd_status==1:
            # -3表示当前容器可能未运行
            return -3
        if add_passwd_status!=0:
            # -1表示当前容器用户已经存在
            return -1
        sum = 0
        flag = 0
        while(flag == 0):
            passwd = subprocess.getoutput("openssl passwd -1 '%s'"%(passwd))
            create_passwd_cmd = "docker exec -u root %s sed -i 's/^%s:!/%s:%s/g' /etc/shadow"%(container_id,user,user,passwd)
            create_passwd_cmd = "docker exec -u root %s sed -i 's/^%s:!/%s:%s/g' /etc/shadow" % (container_id, user, user, passwd)
            # print(create_passwd_cmd)
            add_passwd_status = subprocess.call(create_passwd_cmd, stderr=subprocess.STDOUT, shell=True, env=penv)
            if add_passwd_status == 0:
                flag = 1
            sum += 1
            if sum > 100:
                return -1
        return 1

    # 修改密码
    def docker_change_passwd(self, container_id, user, new_passwd):
        # 得到初始密码
        penv = dict(os.environ)
        get_passwd = "docker exec -u root %s awk -F: '{if($1 == \"%s\") {print $2} }' /etc/shadow"%(container_id,user)
        current_passwd = subprocess.check_output(get_passwd, stderr=subprocess.STDOUT, shell=True, env=penv)
        current_passwd = current_passwd.decode('utf-8').replace('\n','')
        # print(current_passwd.replace('\n',''))
        # 修改密码
        flag = 0
        sum = 0
        while(flag == 0):
            passwd = subprocess.getoutput("openssl passwd -1 '%s'" % (new_passwd))
            create_passwd_cmd = "docker exec -u root %s sed -i 's/^%s:%s/%s:%s/g' /etc/shadow" % (container_id, user,current_passwd, user, passwd)
            print(create_passwd_cmd)
            add_passwd_status = subprocess.call(create_passwd_cmd, stderr=subprocess.STDOUT, shell=True, env=penv)
            if add_passwd_status == 0:
                flag = 1
            sum += 1
            if sum >100:
                return -1
        return 1
# a = Contain()
# c = a.insert_awd_flag('961c7f885b4d','flag{jjusec}','/flag')
# # b = a.docker_change_passwd('e08a9dc21581','glzjin','123456')
# print(c)