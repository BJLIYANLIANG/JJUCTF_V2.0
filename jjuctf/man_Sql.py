import pymysql
import hashlib
from jjuctf.config import Config
config = Config()
import time
class Mysqld:
    def __init__(self):
        server = config.serverIp
        user = config.user
        password = config.password  #数据库密码，宝塔面板
        self.conn = pymysql.connect(server, user, password, config.database)  # 连接到jjuctf数据库
        self.cursor = self.conn.cursor()  #执行方法
        # self.mysqlclose = self.conn.close()
    # 增加用户
    def adduser(self,user_name,password,email):
        sql = 'insert into user (role,password,email,user_name) values ("%d",md5("%s"),"%s","%s")'%(0,password,email,user_name)
        # print(sql)
        #当role为1时表示管理员，0为普通用户，status后面再说
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print("Error for insert to sql")
            # print(sql)
            return -1

        return 1
    #登录时用户验证用户的函数
    def checkuser(self,username,password):
        sql  = 'select user_name from user where user_name="%s" and password=md5("%s")'%(username,password)
        self.cursor.execute(sql)
        # print(sql)
        a = self.cursor.fetchall()
        if a:
            return 1
        else:
            return -1



    #查看整个用户表
    def showuser(self):
        sql = "select * from user"
        self.cursor.execute(sql)
        # print(sql)
        a = self.cursor.fetchall()
        return a

    #注册是检查用户是否被注册过
    def checkUserRegister(self,username):
        sql = 'select user_name from user where user_name="%s" '%(username)
        self.cursor.execute(sql)
        # print(sql)
        a = self.cursor.fetchall()
        if a:
            return 1  #如果用户已经注册，那么返回1
        else:
            return 0




    # 通过选择challenge_list表来
    def selectChallengeListByUserName(self,user):
        try:
            showinfo = self.cursor
            groupid = self.selectGroupidByusername(user)
            # sql = 'select a.id,a.name,a.score,a.hint,a.type,a.docker_flag,a.docker_info,a.file_flag,a.file_path,a.score,a.date,b.solved from challenge_list where group_id=%d or group_id=0' %(groupid)
            sql = 'select a.id,a.name,a.score,a.hint,a.type,a.docker_flag,a.docker_info,a.file_flag,a.file_path,a.date,b.solved,c.solved_flag from (select * from challenge_list where group_id=%d or group_id=0) as a left join (select ctf_exam_id,count(*) as solved from user_challenge_list group by ctf_exam_id) as b on a.ctf_exam_id=b.ctf_exam_id left join (select ctf_exam_id,id as solved_flag from user_challenge_list where group_id=%d) as c on a.ctf_exam_id=b.ctf_exam_id;'%(groupid,groupid)
            showinfo.execute(sql)
            print(sql)
            return showinfo.fetchall()
        except:
            print("selectChallengeListByUserName函数执行失败！")
            return 0



    def selectCtfChallengeTypeNum(self,user):
        groupid = self.selectGroupidByusername(user)
        sql = 'select a.type,count(a.type) from (select * from challenge_list where group_id=%d or group_id=0) as a left join (select ctf_exam_id,count(*) as solved from user_challenge_list group by ctf_exam_id) as b on a.ctf_exam_id=b.ctf_exam_id '%(groupid)
        if groupid!=0:
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                if result:
                    return result
                else:
                    return 0
            except:
                print("查找CTF题目类型出错，赶紧去修复BUG！")
                return 0
        else:
            return 0



    # 这个是用在CTF答题界面中的CTF分类选项中的
    def showChallengeNum(self):
        #用来查看不同类型的题目量
        sql = 'select type,num from challenge_type_num';
        show_challenge_num = self.cursor
        show_challenge_num.execute(sql)
        return show_challenge_num.fetchall()







# ========================group start========================
        #查看队伍信息
    def selectGroupInfoByUsername(self,user):
        try :
            group_id = self.selectGroupidByusername(user)
            if group_id:
                # print("group_id:"+str(group_id))
            # sql = 'select a.group_id,a.name,a.info,b.role from user_group as a left join user_group_list as b on a.group_id = b.group_id and b.user_id=%d'%()
                sql = 'select group_id,name,token,info from user_group where group_id="%s"'%(group_id)
                # print(sql)
                exec = self.cursor
                exec.execute(sql)
                return exec.fetchall()[0]
            return 0
        except:
            return 0

# 通过用户名查队伍id
    def selectGroupidByusername(self, user):
        userid = self.selectUserIdByUserName(user)
        sql = 'select group_id from user_group_list where user_id="%d"'%(userid)
        # print(sql)
        # sql = 'select b.group_id from user as a  join user_group_list as b on a.id=b.user_id and a.user_name="%s";' % (
        #     user)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()[0]
            if result:
                return result
            else:
                return 0
        except:
            return 0
# # 增加队
    def addGroup(self,name,info):
        key = Config().tokenKey
        token = hashlib.md5((name+key).encode('utf-8')).hexdigest()

        a = self.selectGrouInfoByGroupName(name)

        if a:
            return 0
        sql = 'insert into user_group (name,info,token) values ("%s","%s","%s")' % (name,info,token)

        try:

            self.cursor.execute(sql)
            self.conn.commit()
            # self.conn.close()
            return 1
        except:
            self.conn.rollback()
            # self.conn.close()
            return 0



    def addUser_group_list(self,group_id,user_id,role):
        sql = 'insert into user_group_list (group_id,user_id,role) values (%d,%d,%d)' % (group_id, user_id,role)

        try:
            self.cursor.execute(sql)
            self.conn.commit()
            # self.conn.close()
            return 1
        except:
            self.conn.rollback()
            # self.conn.close()
            return 0


    def selectGrouInfoByGroupName(self,groupname):
        sql = 'select group_id,name,token,info from user_group where name="%s";'%(groupname)
        try:

            self.cursor.execute(sql)
            result = self.cursor.fetchall()[0]
            return result
        except:
            return 0

    def selectUserGroupListByGroupId(self,group_id):
        sql = 'select a.user_name,b.role from user as a inner join (select * from user_group_list where group_id=%d) as b on a.id=b.user_id;'%(group_id)
        # print(sql)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        # (('hsm', 1),)
        except:
            return 0
# ========================group end========================




    # 查询用户数
    def selectUserNum(self,user):
        showinfo = self.cursor
        sql = "select * from user"
        showinfo.execute(sql)

        return showinfo.fetchall()


    # 查询用户信息
    def selectUserInfo(self,user):
        sql = 'select id,user_id,real_name,role,status,email,mobile,class_id,user_photo from user where user_name="%s"'%(user)
        showinfo = self.cursor
        try:
            showinfo.execute(sql)
            return showinfo.fetchall()[0]
        except:
            return 0



    # 查看所有靶机
    def select_target(self):
        showinfo = self.cursor
        sql = "SELECT * FROM `target`"
        showinfo.execute(sql)
        return showinfo.fetchall()

    # 检查admin登录用户
    def checkAdminLogin(self,username,password):
        sql = 'select admin_id from admin where admin_name="%s" and admin_password=md5("%s")' % (username, password)
        self.cursor.execute(sql)

        a = self.cursor.fetchall()
        if a:
            return 1
        else:
            return -1

    # 通过用户名查用户id
    def selectUserIdByUserName(self,user):
        sql = 'select id from user where user_name="%s"'%(user)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return 0



    def selectCtfTypeAndScoreByChallenge_id(self,ctf_id):
        # adduserscore.addUserScore(user, group_id, ctfType, ctf_id, user_id, score, date)
        sql = 'select type,score from challenge_list where id="%s"'%(ctf_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()[0]
        if result:
            type = result[0]
            score = result[1]
            return type,score
        else:
            return 0



    #ctf公告
    def selectUserNotice(self):
        sql = 'select id,info,date from user_notice'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

# ===============后台-start===============
    def addAdmin(self,name,email,mobile,passwd):
        sql = 'insert into admin (admin_name,admin_email,admin_mobile,admin_password) values("%s","%s","%s",md5("%s"))'%(name,email,mobile,passwd)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.conn.close()

        result = self.cursor.fetchall()


        return result

    def selectAdminList(self):
        sql = 'select admin_id,admin_name,admin_email,admin_mobile,status from admin'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print(result)
        if result:
            return result
        return 0

    # 通过管理员名字查管理员id
    def selectAdminIdByAdminName(self,name):
        sql =  'select admin_id from admin where admin_name="%s"'%(name)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()[0]
            if result:
                # 返回一个整数
                return result
            return 0
        except:
            print("查找管理员id失败,请检查函数:selectAdminIdByAdminName!")
            return 0




    def selectUserList(self):
        sql = 'select id,user_name,real_name,class_id,email,mobile from user'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0


    def selectCtfInstanceList(self):
        sql = 'select group_id,id,ctf_exam_id,name,score,hint,type,docker_flag,docker_info,file_flag,file_path,flag,date,flag from challenge_list'
        # print(sql)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return  result
        except:
            return 0


    def checkFalg(self,flag,challenge_id):
        sql = 'select * from challenge_list where flag="%s" and id=%d'%(flag,challenge_id)
        # print(sql)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if result:
                return 1
            else:
                return 0
        except:
            return 0

    #增加用户得分
    # user_challenge_list
    def addUserScore(self, group_id, ctfType, challenge_id, user_id, score, date):
        #首先获取题目的CTF_id
        sql = 'select ctf_exam_id from challenge_list where id=%d'%(challenge_id)
        self.cursor.execute(sql)
        query_ctf_exam_id = self.cursor.fetchone()
        if query_ctf_exam_id[0]==None:
            return 0
        sql = 'insert into user_challenge_list (group_id,type,challenge_id,user_id,score,date,ctf_exam_id)values(%d,%d,%d,%d,%d,"%s",%d)'%(group_id,ctfType,challenge_id,user_id,score,date,query_ctf_exam_id[0])
        print(sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return 1

        except:
            self.conn.rollback()
            return 0

    def selectUserScoreListByGroupId(self,group_id):
        sql = 'select c.name,a.type,b.user_name,a.score,a.date from user_challenge_list as a left join user as b on a.user_id=b.id left join ctf_exam as c on c.id=a.ctf_exam_id where a.group_id=%d'%(group_id)
        try:
            self.cursor.execute(sql)
            userScoreList = self.cursor.fetchall()
            return userScoreList

        except:
            self.conn.rollback()
            return 0
    #user_score_list表
    # def addUserScoreList(self,uid,gid,challenge_id,score):
    #     date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     sql = ''
    #     #答题成功后添加到这个表中


    def selectctf_exam(self):
        sql = ' SELECT id,own_id,type,name,hint,base_score,flag_type,base_flag,file_flag,file_path,docker_flag,docker_path,create_time,info,status FROM `ctf_exam`;'
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
#返回类型: ((1, 13,0, ' easyPython', 'easyPython', 50, 0, 'flag{xxxxx123}', 0, None, 0, 'easyPython', datetime.datetime(2020, 12, 1, 0, 0), None,0),)
        except:
            return 0


    def selectctf_examByctf_exam_Id(self,id):
        sql = ' SELECT id,own_id,type,name,hint,base_score,flag_type,base_flag,file_flag,file_path,docker_flag,docker_path,create_time,info,status FROM `ctf_exam` where id=%d;'%(id)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return 0
        # (1, 13, 0, ' easyPython', 'easyPython', 50, 0, 'flag{xxxxx123}', 0, None, 1, 'easyPython',datetime.datetime(2020, 12, 1, 0, 0), None, 0)
        except:
            return 0
    def select_user_challenge_list(self):
        sql = 'select * from user_challenge_list'
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except:
            return 0
    def add_user_challenge_list(self,group_id,ctf_exam_id):
        #如果group_id==0表示这个是静态flag，并且只要创建一个就行
        if group_id==0:
            #ddd
            ctf_exam_info = self.selectctf_examByctf_exam_Id(ctf_exam_id)
            if ctf_exam_info:
                if ctf_exam_info[10]==0:  #当docker_flag为0的时候，也就是不需要开启docker的题目
                    own_id = ctf_exam_info[1]
                    type = ctf_exam_info[2]    #题目类型 如web misc等
                    name = ctf_exam_info[3]
                    hint = ctf_exam_info[4]
                    score = ctf_exam_info[5]
                    flag = ctf_exam_info[7]
                    file_flag = ctf_exam_info[8]
                    file_info = ctf_exam_info[9]
                    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    info = ctf_exam_info[13]
                    sql = 'insert into challenge_list (group_id,ctf_exam_id,name,score,hint,type,docker_flag,file_flag,file_path,flag,date) values (%d,%d,"%s",%d,"%s",%d,%d,%d,"%s","%s","%s")'%(group_id,ctf_exam_id,name,score,hint,type,0,file_flag,file_info,flag,datetime)
                    sql2 = 'update ctf_exam set status=1 where id=%d;'%(ctf_exam_id)
                    try:
                        print(sql)
                        self.cursor.execute(sql)
                        self.cursor.execute(sql2)
                        self.conn.commit()
                        self.conn.close()
                        return 1
                    except:
                        print("add_user_challenge_list(self,group_id,ctf_exam_id)函数执行错误！")
                        self.conn.rollback()
                        self.conn.close()
                        return 0
        else:
            return 0
    #情况CTf成绩表内容
    def delEntireUser_Challenge_list(self):
        sql = 'TRUNCATE table `jjuctf`.`user_challenge_list`'
        try:
            self.cursor.execute(sql)
            self.cursor.fetchall()
            self.conn.commit()
            return 1
        except:
            self.conn.rollback()
            self.conn.close()
            return 0
    #删除管理员用户
    def delAdminById(self,id):
        sql = 'DELETE FROM `admin` WHERE admin_id =%d'%(id)
        # print(sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            self.conn.close()
            return 1
        except:
            self.conn.rollback()
            self.conn.close()
            print("删除管理员信息失败!")
            return 0
    #禁用管理员
    def changeAdminStatusById(self,id):
        # status=0为禁用，已经在数据库中设置status默认为1
        checksql = 'select status from admin where admin_id=%d'%(id)
        self.cursor.execute(checksql)
        status = self.cursor.fetchone()[0]
        print()
        print(status)
        if status==0:
            sql = 'update `admin` set status=1  WHERE admin_id =%d' % (id)
        else:
            sql = 'update `admin` set status=0  WHERE admin_id =%d' % (id)
        print(sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            self.conn.close()
            return 1
        except:
            self.conn.rollback()
            self.conn.close()
            print("禁用管理员信息失败!")
            return 0

    def delUserCtfExam(self,ctf_exam_id):
        sql = 'delete from ctf_exam where id=%d'%(ctf_exam_id)
        # sql2 =  'select id from challenge_list where id=%d'%(ctf_exam_id)# 首先
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            self.conn.close()
            return 1
        except:
            self.conn.rollback()
            self.conn.close()
            print("删除数据表失败!")
            return 0


    #删除CTF实例
    def delUserCtfInstanceById(self,id):
        sql = 'delete from challenge_list where id=%d'%(id)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            self.conn.close()
            return 1
        except:
            self.conn.rollback()
            self.conn.close()
            print("删除数据表失败!")
            return 0

    def addUserCtfExam(self,own_id,type,name,hint,base_score,status,flag_type,base_flag,file_flag,file_path,docker_flag,docker_path,info):
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = 'insert into ctf_exam (own_id,type,name,hint,base_score,status,flag_type,base_flag,file_flag,file_path,docker_flag,docker_path,create_time,info) values (%d,%d,"%s","%s",%d,%d,%d,"%s",%d,"%s",%d,"%s","%s","%s")'%(own_id,type,name,hint,base_score,status,flag_type,base_flag,file_flag,file_path,docker_flag,docker_path,create_time,info)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            self.conn.close()
            return 1
        except:
            self.conn.rollback()
            self.conn.close()
            print("插入数据表失败!")
            return 0

    # def selectUserGroupList(self):
    #     sql = 'select group_id,name,info,create_time from user_group'
    #     try:
    #         self.cursor.execute(sql)
    #         result = self.cursor.fetchall()
    #         return result
    #     except:
    #         return 0

    #当status为0时表示比赛没结束或者未开始
    def selectCompetition_InfoByStatus(self,statusNum):
        sql = 'select status,name,info,start_date,end_date from competition where status=%d'%(statusNum)
        # print(sql)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except:
            return 0
    def selectCompetitionInfoList(self):
        sql = 'select status,name,info,start_date,end_date from competition'
        # print(sql)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except:
            return 0
    def changeCompetitionInfo(self,name,info,start_date,end_date):
        sql = 'change table '

# ===============后台-end===============

# 间可以使用‘+’，‘*’,即允许元组进行组合连接和重复复制，运算后生成一个新的元组。



# ===============user-start===============


# 完整内容
# id
# group_id
# ctf_exam_id
# type
# challenge_id
# user_id
# score
# date

# # ===============user-end===============
# a = Mysqld()
# b = a.selectUserScoreListByGroupId(45)
# print(b)
# b = a.addUserCtfExam(12,0,"testWEB","this hint",100,0,0,"flag{helloworld}",1,"https://www.hsm.cool",0,0,"this is test!")
# b = a.selectAdminIdByAdminName('hsm')
# print(b)