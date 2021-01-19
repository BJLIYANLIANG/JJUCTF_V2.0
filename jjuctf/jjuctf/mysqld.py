import pymysql
import jjuctf.config

class Mysqld:
    def __init__(self):
        server = "localhost"
        user = "jjuctf"
        password = "jjuctf"  #数据库密码，宝塔面板
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
        sql  = 'select user_name from user where user_name="%s" and password=md5("%s")'%(username,password)
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
        sql = "select * from user"
        showinfo.execute(sql)
        # print(showinfo.fetchall())
        return showinfo.fetchall()

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
        print(sql)
        a = self.cursor.fetchall()
        if a:
            return 1
        else:
            return -1
