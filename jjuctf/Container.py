import os
import time
import re
import base64
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
            return -1


# test
    def docker_stop_by_docker_id(self,dockerID):
        penv = dict(os.environ)
        try:
            subprocess.Popen(['docker','stop',dockerID],shell=False,env=penv)
            return 1
        except subprocess.CalledProcessError as e:
            print(e.output)
            return -1


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
        cmd = 'docker run --rm --network=awd --ip %s  -d  %s'%(ip,images_id)
        print(cmd)
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, env=penv)
            return str(result)[2:14]
        except subprocess.CalledProcessError as e:
            print(e.output)
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
            if os.name == 'nt':
                cmd = "wsl openssl passwd -1 '%s'" % (passwd)
            else:
                cmd = "openssl passwd -1 '%s'"%(passwd)
            # passwd = subprocess.getoutput()
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
        # 定义变量
        flag = 0
        sum = 0
        # 得到容器中的初始密码
        penv = dict(os.environ)
        shell = '''awk -F: '{if($1 == "%s") {print $2} }' /etc/shadow''' % (user)
        # print(shell)
        # current_passwd
        # print('shell:',shell)
        current_passwd = self.docker_exec_get_return(container_id,shell)
        # print('current_passwd:',current_passwd)
        # 修改密码

        while(flag == 0):
            # 生成新密码 nt表示windows系统，则使用wsl中的linux生成密码
            if os.name == 'nt':
                shell = "wsl openssl passwd -1 '%s'" % (new_passwd)
            else:
                # Linux 系统
                shell = "openssl passwd -salt '12345678' -1 '%s'" % (new_passwd)
            new_passwd = subprocess.getoutput(shell)
            new_passwd = new_passwd.replace('/','\/')
            new_passwd = new_passwd.replace('.','\.')
            # print('newpasswd:',new_passwd)
            # 修改密码，将旧密码替换成新密码
            shell = "sed -i 's/^%s:%s/%s:%s/g' /etc/shadow"% (user,current_passwd, user, new_passwd)
            # print(shell)
            # 返回执行状态，0表示成功执行，
            status_code = self.docker_exec_return_status_code(container_id,shell)
            if status_code == 0:
                # print('成功插入密码')
                flag = 1
            sum += 1
            if sum >100:
                return -1
        return 1




    # 检查这个镜像是否在这个系统中
    def search_docker_image_in_system(self,image_id):
        cmd = 'docker images'
        a = subprocess.getoutput(cmd)
        if image_id in a:
            return 1
        else:
            return -1

    def show_docker_version(self):
        cmd = 'docker --version'
        result = subprocess.getoutput(cmd)
        return  result



    def docker_clean(self):
        containers = subprocess.getoutput('docker ps -a -q')
        # print(containers)
        if containers:
            print("[DOCKER] Stop and remove all contaners: ")
            for container in containers.split():
                subprocess.call(["docker", "stop", container])
                subprocess.call(["docker", "rm", "-f", container])
        else:
            print("[DOCKER] No containers")



    # 返回执行结果
    def docker_exec_get_return(self,container_id,shell):
        penv = dict(os.environ)
        try:
            shell_base64_encode = self.docker_shell_base64(shell)
            shell = "echo {0} | base64 -d|bash".format(shell_base64_encode)
            cmd = '''docker exec -u root {0} /bin/bash -c "{1}"'''.format(container_id,shell)
            # passing = ['docker', 'exec', '-u', 'root', container_id, '/bin/bash', '-c', shell]
            # print(passing)
            b = subprocess.getoutput(cmd)
            # print(b.stdout)

            return b
        except Exception as e:
            print(e)
            return -1



    # 执行shell，并且返回执行结果
    def docker_exec_return_status_code(self,container_id,shell):
        try:
            shell_base64_encode = self.docker_shell_base64(shell)
            shell = "echo {0} | base64 -d|bash".format(shell_base64_encode)
            b = subprocess.run(['docker', 'exec', '-u', 'root', container_id, '/bin/bash', '-c', shell])
            # 0表示成功执行
            # subprocess.getstatusoutput()
            return b.returncode

        except:
            return -1



    def docker_del_container(self,container_id):
        try:
            b = subprocess.run(['docker', 'rm', container_id])
            return b.returncode
        except:
            return -1


    def docker_shell_base64(self,shell):
        return base64.b64encode(str(shell).encode('utf-8')).decode('utf-8')


    def docker_stop_container_by_list(self,container_list):
        for container_id in container_list:
            try:
                self.docker_stop_by_docker_id(container_id)
            except Exception as e:
                print(e)
                return -1
        return 1


