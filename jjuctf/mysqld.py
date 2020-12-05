import pymysql
class Mysqld:
    def __init__(self):
        server = "101.200.138.126"
        user = "jjuctf"
        password = "ibJdJc6tXdRfmaRL"
        self.conn = pymysql.connect(server, user, password, database="jjuctf")  # 连接到jjuctf数据库
        self.cursor = self.conn.cursor()  #执行方法
    def addUser(self,userName,userEmail,userPassword):
        sql = 'insert into userlogin (user_name,user_email,user_password) values ("%s" ,"%s",md5("%s"))'%(userName,userEmail,userPassword)
        try:
            self.cursor.execute(sql)
            self.conn.commit()

        except:
            print("Error for insert to sql")
            return -1

        return 1

    def checkUser(self,username,password):
        sql = 'select user_name from userlogin where user_name="%s" and user_password=md5("%s")'%\
              (username,password)
        self.cursor.execute(sql)
        a = self.cursor.fetchall()
        print(type(a))
        if a :
            return 1
        else:
            return -1
    def checkUserRegister(self,username):
        sql = 'select user_name from userlogin where user_name="%s" '%(username)
        self.cursor.execute(sql)
        # print(sql)
        a = self.cursor.fetchall()
        if a:
            return 1  #如果用户已经注册，那么返回1
        else:
            return 0
    def showuserinfo(self):
        showinfo = self.cursor
        showinfo.execute("select * from userlogin where user_name=")
        return self.cursor.fetchall()


    # 通过选择challenge_list表来
    def selectinfo(self,type):
        showinfo = self.cursor
        sql = "select * from challenge_list where challenge_type=%d"%(type)
        sql = "select * from challenge_list"
        showinfo.execute(sql)


        return showinfo.fetchall()

    def selectUserNum(self,):  #查询用户数
        showinfo = self.cursor
        sql = "select * from userlogin"
        showinfo.execute(sql)
        # print(showinfo.fetchall())

        return showinfo.fetchall()
    def select_target(self):
        showinfo = self.cursor
        sql = "SELECT * FROM `target`"
        showinfo.execute(sql)
        return showinfo.fetchall()
# a = Mysqld()
# aa  = a.addUser(userName="user1",userEmail="sadfds@gmail.com",userPassword="123456")
# print(aa)
a = Mysqld()
b = a.select_target()
# print(b)
for i in b:
    print(i)
# a1 = []
# for i in b:
#     if i[4] == 0:
#         a1.append(i)
# print(a1)
# print(a1[0][2])
# for i in a:
#     print(i)


# 队号 用户  分数
#
# 队号 解体数量


