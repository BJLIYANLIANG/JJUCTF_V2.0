from jjuctf.SqlServer import Mysqld
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
    mysql = Mysqld()
    ip_pool = mysql.select_ip_pool()
    start_ip = ip_pool[0]
    end_ip = ip_pool[1]
    point_ip = ip_pool[2]
    # ip都已经分配完毕
    if point_ip == end_ip:
        return -1
    else:
        split_ip = point_ip.split('.')
        tmp0 = split_ip[0]
        tmp1 = split_ip[1]
        tmp2 = split_ip[2]
        tmp3 = int(split_ip[3])
        tmp3= tmp3 + 1
        next_point_ip = tmp0+'.'+tmp1+'.'+tmp2+'.'+str(tmp3)
        mysql.update_ip_pool(next_point_ip)
        return point_ip

# 释放docker ip
def docker_release_ip():
    mysql = Mysqld()
    ip_pool = mysql.select_ip_pool()
    start_ip = ip_pool[0]
    end_ip = ip_pool[1]
    point_ip = ip_pool[2]
    # ip都已经释放完毕
    if point_ip == start_ip:
        return -1
    else:
        split_ip = point_ip.split('.')
        tmp0 = split_ip[0]
        tmp1 = split_ip[1]
        tmp2 = split_ip[2]
        tmp3 = int(split_ip[3])
        tmp3= tmp3 - 1
        next_point_ip = tmp0+'.'+tmp1+'.'+tmp2+'.'+str(tmp3)
        mysql.update_ip_pool(next_point_ip)
        return next_point_ip
