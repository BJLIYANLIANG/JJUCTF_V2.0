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
    def showChallengeList(self,user):
        userId = self.selectUserId(user)
        showinfo = self.cursor
        sql = 'select a.challenge_id,a.challenge_name,a.challenge_score,a.challenge_hint,a.challenge_type,a.docker_flag,a.docker_path,a.challenge_flag,a.challenge_file,a.solved_num,b.score from challenge_list  as a left join (select * from user_challenge_list where user_id="%s") as b on a.challenge_id = b.challenge_id;'%(userId)
        showinfo.execute(sql)
        return showinfo.fetchall()

    # 这个是用在CTF答题界面中的CTF分类选项中的
    def showChallengeNum(self):
        #用来查看不同类型的题目量
        sql = 'select type,num from challenge_type_num';
        show_challenge_num = self.cursor
        show_challenge_num.execute(sql)
        return show_challenge_num.fetchall()



    def selectGroupInfoByUser(self,user):
        group_id = self.selectGroupByusername(user)
        if group_id:
            sql = 'select * from user_group where group_id="%s"'%(group_id)
            exec = self.cursor
            exec.execute(sql)
            return exec.fetchall()
        else:
            return 0

    # 查询用户数
    def selectUserNum(self,user):
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
    #
    # def selectUserChallengeDockerAllby(self):
    #     sql = "select a.challenge_id,a.challenge_name,a.challenge_score,a.challenge_hint,a.challenge_type,a.docker_flag,a.docker_path,a.challenge_flag,a.challenge_file,a.solved_num,b.score from challenge_list  as a left join (select * from user_challenge_list where user_id=15) as b on a.challenge_id = b.challenge_id;"
    #     self.cursor.execute(sql)
    #     print(sql)
    #     a = self.cursor.fetchall()
    #     print(a)

    # 通过用户名查用户id
    def selectUserId(self,user):
        sql = 'select id from user where user_name="%s"'%(user)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if result:
            return result[0][0]
        return 0
    # 通过用户名查队伍名
    def selectGroupByusername(self,user):
        sql = 'select group_id from user where user_name="%s"'%(user)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if result:
            return result[0][0]
        else:
            return 0

# ===============后台-start===============
    def addAdmin(self,name,email,mobile,passwd):
        sql = 'insert into admin (admin_name,admin_email,admin_mobile,admin_password) values("%s","%s","%s",md5("%s"))'%(name,email,mobile,passwd)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.conn.close()
        print(sql)
        result = self.cursor.fetchall()

        print(result)
        return result
    def selectAdminList(self):
        sql = 'select admin_id,admin_name,admin_email,admin_mobile from admin'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0

    def selectUserList(self):
        sql = 'select id,user_name,real_name,class_id,email,mobile from user'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if result:
            return result
        return 0
    def selectCTFList(self):
        sql = 'select challenge_id,challenge_name,challenge_score,challenge_hint,challenge_type,docker_flag,docker_path,challenge_flag,challenge_file,solved_num from challenge_list'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return  result
# ===============后台-end===============



# ===============user-start===============

# ===============user-end===============
# a = Mysqld()
# b = a.selectCTFList()
# # c = a.showChallengeList()
# # d = a.showChallengeNum()
# # print(c)f
# # print(b)
#
# print(b)