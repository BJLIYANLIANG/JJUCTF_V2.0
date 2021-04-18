from jjuctf.SqlServer import Mysqld
import hashlib
import random
import datetime
import requests
from jjuctf.Container import *
ip_pool = []



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
    print('groupname_list:',groupname_list)
    # 清楚所有数据
    status_code = mysql.delete_awd_ranks_all()
    if status_code==0:
        return -1
    else:
        # 构造查询语句
        base = 'INSERT INTO awd_ranks (group_name,score) VALUES'
        flag = 0
        for i in groupname_list:
            str1 = ' ("%s","%s")'%(str(i[0]),str(init_score))
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


def check_awd_status_by_url(url):
    requests.get()




