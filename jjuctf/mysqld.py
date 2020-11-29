import pymysql
class Mysqld:
    def __init__(self):
        server = "127.0.0.1"
        user = "root"
        password = "905008"
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
    def select
# a = Mysqld()
# aa  = a.addUser(userName="user1",userEmail="sadfds@gmail.com",userPassword="123456")
# print(aa)





