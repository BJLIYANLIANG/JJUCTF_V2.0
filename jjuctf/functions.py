from jjuctf.SqlServer import Mysqld
import hashlib
import random
import datetime
from jjuctf.Container import *
ip_pool = []
# ip_pool.append('127.0.0.2')
#
# print(ip_pool)
# ip_pool.pop()
# print(ip_pool)
# ip_pool.pop()
#
# print(ip_pool)
def init_ip_pool():
    for i in range(2,255):
        ip = '172.18.0.'+str(i)
        ip_pool.append(ip)

# 查找CTF排名用的，大概用在app.py的400行
def ctf_search_rank(group_name):
    mysql = Mysqld()
    a = mysql.selectUserChallengeListDesc()
    j = 1
    # print(a)
    for i in a:
        if i[0] == group_name:
            return j
        else:
            j += 1
    return j

#awd 初始化排行榜
def init_awd_ranks(init_score):
    mysql = Mysqld()
    groupname_list = mysql.select_groupname_list()
    # 清楚所有数据
    status_code = mysql.delete_awd_ranks_all()
    if status_code==0:
        return -1
    else:
        # 构造查询语句
        base = 'INSERT INTO awd_ranks (group_name,score) VALUES '
        flag = 0
        for i in groupname_list:
            str1 = '("%s","%s")'%(str(i[0]),str(init_score))
            if flag == 0:
                base += str1
                flag = 1
            else:
                base += ','
                base += str1
        result = mysql.exec(base)
        if result == 1:
            return 1
        else:
            return -1
# init_awd_ranks(5000)

def docker_get_ip():

    # mysql = Mysqld()
    # ip_pool = mysql.select_ip_pool()
    # start_ip = ip_pool[0]
    # end_ip = ip_pool[1]
    # point_ip = ip_pool[2]
    # # ip都已经分配完毕
    # if point_ip == end_ip:
    #     return -1
    # else:
    #     split_ip = point_ip.split('.')
    #     tmp0 = split_ip[0]
    #     tmp1 = split_ip[1]
    #     tmp2 = split_ip[2]
    #     tmp3 = int(split_ip[3])
    #     tmp3= tmp3 + 1
    #     next_point_ip = tmp0+'.'+tmp1+'.'+tmp2+'.'+str(tmp3)
    #     mysql.update_ip_pool(next_point_ip)
    #     return point_ip
    return ip_pool.pop()

# 释放docker ip
def docker_release_ip(ip):
    ip_pool.append(ip)
    return 1

#加密方法
def get_md5(s):
  return hashlib.md5(s.encode('utf-8')).hexdigest()


def get_random_password(str_user):
    salt = str(random.randint(1,1000))
    salt2 = 'hsmcool'
    return get_md5(salt+str_user+salt2)[:12]



# 打开awd实例
def start_awd_instance_for(group_list,images_id,name,ssh_port,other_port,ssh_user):
    docker = Contain()
    mysql = Mysqld()
    now_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ip_dic = {}
    print(now_time)
    # 得到ip
    try:
        for i in group_list:
            print(ip_pool)
            # 从ip池中获取一个ip
            ip = docker_get_ip()
            print('image_id:',images_id)
            container_id = docker.docker_start_by_imagesID('tag',images_id,ip)
            print('ip:',ip,'container_id:',container_id)
            if container_id == -1:
                return -1
            # 这里修改docker用户密码
            passwd = get_random_password(ssh_user)
            result = docker.docker_change_passwd(container_id,ssh_user,passwd)

            if result == -1:
                return -1
            status_code = mysql.insert_awd_instance(container_id, name, ssh_port, other_port, now_time, '',ip,'tag',i[1],1,ssh_user,passwd)

        return 1
    except:
        return -1


