import pymysql
class Mysqld:
    def __init__(self):
        server = "127.0.0.1"
        user = "root"
        password = "905008"
        self.conn = pymysql.connect(server, user, password, database="jjuctf")  # 连接到jjuctf数据库
        self.cursor = self.conn.cursor()  #执行方法
    def addUser(self,userName,userEmail,userPassword):

        a = 'insert into userlogin (user_name,user_email,user_password) values ("%s" ,"%s",md5("%s"))'%\
            (userName,userEmail,userPassword)
        try:
            self.cursor.execute(a)
            self.conn.commit()
        except:
            print("Error for insert to sql")
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







