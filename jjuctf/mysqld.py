import pymysql
class Mysqld:
    def __init__(self):
        server = "101.200.138.126"
        user = "jjuctf"
        password = "ibJdJc6tXdRfmaRL"  #数据库密码，宝塔面板
        self.conn = pymysql.connect(server, user, password, database="jjuctf")  # 连接到jjuctf数据库
        self.cursor = self.conn.cursor()  #执行方法

    # 增加用户
    def adduser(self,user_id,user_name,real_name,password,email,mobile,class_id,user_photo,role):
        sql = 'insert into user (user_id,real_name,role,status,password,email,mobile,class_id,user_photo,user_name) ' \
              'values ("%s","%s","%d","%d",md5("%s"),"%s","%s","%d","%s","%s")'\
              %(user_id,real_name,role,0,password,email,mobile,class_id,user_photo,user_name)
        print(sql)
        #当role为1时表示管理员，0为普通用户，status后面再说
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print("Error for insert to sql")
            print(sql)
            return -1

        return 1
    #登录时用户验证用户的函数
    def checkuser(self,username,password):
        sql  = 'select user_name,role from user where user_name="%s" and password=md5("%s")'%(username,password)
        self.cursor.execute(sql)
        print(sql)
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
    def selectinfo(self,type):
        showinfo = self.cursor
        sql = "select * from challenge_list where challenge_type=%d"%(type)
        sql = "select * from challenge_list"
        showinfo.execute(sql)


        return showinfo.fetchall()

    # 查询用户数
    def selectUserNum(self,):
        showinfo = self.cursor
        sql = "select * from userlogin"
        showinfo.execute(sql)
        # print(showinfo.fetchall())
        return showinfo.fetchall()

    # 查看所有靶机
    def select_target(self):
        showinfo = self.cursor
        sql = "SELECT * FROM `target`"
        showinfo.execute(sql)
        return showinfo.fetchall()
# a = Mysqld()
# aa  = a.addUser(userName="user1",userEmail="sadfds@gmail.com",userPassword="123456")
# print(aa)
# a = Mysqld()
# b = a.select_target()
# # print(b)
# for i in b:
#     print(i)
# a1 = []
# for i in b:
#     if i[4] == 0:
#         a1.append(i)
# print(a1)
# print(a1[0][2])
# for i in a:
#     print(i)
#
# a = Mysqld()
# b = a.addadmin("20180201420","hsm","贺述明","905008","905008677@qq.com","18579266908",1861,"")
# print(b)
# print(str(a))
# b = a.checkUser("HSM","905008")
# # b = a.showuser()
# b = a.checkuser("hsm","905008")
# print(b)
# print(b)
# 队号 用户  分数
# 队号 解体数量


# select user_name,role from user where user_name="hsm" and password=md5("905008")
#