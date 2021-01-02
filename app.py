from flask import Flask,url_for
from flask import render_template
from  flask import request,flash
from  flask import session,redirect
from datetime import timedelta
from jjuctf.man_Sql import Mysqld
from werkzeug.utils import secure_filename
import os
from jjuctf.Check import Check
import time
app = Flask(__name__)
app.secret_key = '905008'  #session 密钥
app.debug = True


# 常量
app.config['UPLOAD_FOLDER'] = 'static/'




@app.route('/login',methods=['GET','POST'])
def login():
    if session.get("user"):
        return render_template("user/index.html")
    if request.method == 'GET':
        return render_template('user/login.html')
    if request.method == 'POST':
        
        username = request.form.get('username')
        password = request.form.get('password')

        if username == '' or password == '':  #检查用户名和密码是否为空
            return render_template("user/login.html",message="用户名或密码不能为空")
        checkuser = Mysqld()

        result = checkuser.checkuser(username,password) #对用户表进行操作，检查登录
        if result == 1:
            session.permanent = True  #设置session为永久的
            app.permanent_session_lifetime = timedelta(minutes=20)  # 设置session到期时间，单位分钟
            session['user'] = request.form.get('username')
            return redirect('/')
        else:
            return render_template("user/login.html",message="帐号或密码错误")
    else:
        return redirect('/login')


# ctf解题模式
@app.route('/challenges')
def challenge():
    user = session.get('user')
    if user :  #如果登录成功
        getChallengeListByType = Mysqld()
        #获取CTf实例列表
        challengeResult = getChallengeListByType.selectChallengeListByUserName(user)
        print("challengeResult:",end='')
        print(challengeResult)
        challengeNum = getChallengeListByType.showChallengeNum()
        # challengeTypeNum = getChallengeListByType.selectCtfChallengeTypeNum(user)   #用这个代替上面那个！今天不写了，难受，我写的垃圾代码。。。
        groupInfo = getChallengeListByType.selectGroupInfoByUsername(user)
        # print(groupInfo)
        userNotice = getChallengeListByType.selectUserNotice()
        # print(userNotice)
        # 0为web 以此类推
        return render_template("user/challenge.html",username=user,headerType="challenges",challengeResult=challengeResult,
                               examNum=challengeNum,groupInfo=groupInfo,userNotic=userNotice)
    return render_template('user/login.html')



# index
# ctf解题模式
@app.route('/')
@app.route('/index')
def index():
    user = session.get('user')
    if user :  #如果登录成功
        return render_template("user/index.html",username=user,headerType="index")
    return render_template('user/index.html',headerType="index")

@app.route('/ranks')
def ranks():
    user = session.get('user')
    if user:
        sqlcheck = Mysqld()
        GetChallengeList = sqlcheck.showChallengeList(user)
        # GetGroupInfo  = sqlcheck.
        GetUserNum = sqlcheck.selectUserNum(user)  #查数据库将排行榜数据传到template中，目前是测试阶段，使用的是用户表

        return render_template("user/ranks.html",username=user,headerType="rank",ChallengeList=GetChallengeList,userNum=GetUserNum,a=1)
    else:
        return render_template("user/login.html")

@app.route('/register',methods=['POST','GET'])
def userRegister():
    if request.method != 'POST':   #用户不是使用
        return render_template("user/register.html")
    else:
        uid = request.form.get('uid')
        username = request.form.get('username')
        realname = request.form.get('realname')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        class_id = request.form.get('classid')
        passwd = request.form.get('passwd')
        passwd2 = request.form.get('passwd2')

        def eheck(passwd,):  #这个函数用来代替下面的代码验证字符串
            pass

        resultEmpty = 0
        # result = checkstr.checkUserString(username=username,password=passwd,useremail=email,)  #检查用户输入的字符串
        if passwd2 == '' or passwd == '' or username == '' or email == '' or mobile == '' or uid == '' or realname == ''  or class_id == '':
            resultEmpty = 1

        if passwd != passwd2:
            return render_template("user/register.html",message="两次输入的密码不同，请重新输入")

        if resultEmpty == 1:
            return render_template("user/register.html",message="提交异常，请重新输入")
        adduser = Mysqld()
        if adduser.checkUserRegister(username=username) == 1:
            return render_template("user/register.html",message="用户已经注册过!")
        result1 = adduser.adduser(username,passwd,email)
        if result1 == 1:
            return render_template("user/login.html",message="注册成功，请到队伍管理添加队伍！")



@app.route("/logout")
def logout():
    session.clear()
    return render_template("user/login.html",message="退出帐号成功，请重新登录")


# AWD模块
@app.route('/awd')
def awd():
    user = session.get('user')
    if user:
        return render_template("user/awd.html",username=user,headerType="awd")
    else:
        return render_template("user/login.html")


# 用户个人设置
@app.route('/user',methods=['GET'])
def user():
    user = session.get('user')
    if user:
        username = request.args.get('user')
        mysql = Mysqld()
        userinfo = mysql.selectUserInfo(user)
        # print(userinfo)
        usergroupinfo = mysql.selectGroupInfoByUsername(user)
        # print(usergroupinfo)
        # print(usergroup)
        return render_template("user/user.html",username=username,headerType=username,userinfo=userinfo,usergroupinfo=usergroupinfo)
    else:
        return render_template("user/login.html")


# 队伍设置
@app.route('/group',methods=['GET'])
def groupSetting():
    user = session.get('user')
    if user:
        username = request.args.get('user')
        mysql = Mysqld()
        userinfo = mysql.selectUserInfo(user)
        groupinfo = mysql.selectGroupInfoByUsername(user)
        print(user)
        print(groupinfo)
        #
        if groupinfo:
            groupList = mysql.selectUserGroupList(groupinfo[0])
            print(groupList)
        # print(userinfo)
            return render_template("user/group.html",username=username,headerType="userSetting",userinfo=userinfo,groupinfo=groupinfo,groupList=groupList)
        else:
            return render_template("user/group.html",username=username,headerType="userSetting",userinfo=userinfo,groupinfo=groupinfo)

    else:
        return render_template("user/login.html")




@app.route('/practice')
def practice():
    user = session.get('user')
    if user:
        return render_template("user/pratices.html",username=user,headerType="practice")
    else:
        return render_template("user/login.html")

@app.route('/exams')
def exams():
    user = session.get('user')
    if user:
        return render_template("user/exam.html",username=user,headerType="exam")
    else:

        return render_template("user/login.html")


@app.route("/settings")
def setting():
    return render_template("user/index.html")





# 检查CTF答题模式flag是否正确
# 通过ajax验证
@app.route("/checkCtfFlag",methods=["POST"])
def checkCtfFlag():
    # 检查flag需要ctf_id这个参数
    user = session.get("user")
    flag = request.form.get('flag')
    ctf_id = int(request.form.get('ctf_id'))
    print(ctf_id)
    print(flag)
    if user:
        if flag and ctf_id :
            # ctf_id就是CTF靶场id
                # 没创建一个题目都会创建一个或者多个ctf_id,静态flag只需要创建一个id即可
            a = Mysqld()
            result = a.checkFalg(flag, ctf_id)
            # result = 1
            #如果result为1则正确，0为不正确
            print(result)

            if result == 1:
                mysql = Mysqld()
                group_id = mysql.selectGroupInfoByUsername(user)[0]
                print(group_id)
                if group_id != 0:
                    (ctfType,score) = mysql.selectCtfTypeAndScoreByChallenge_id(ctf_id)
                    print(ctfType,score)
                    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print(date)
                    print(user)
                    # mysql1 = Mysqld()
                    user_id = mysql.selectUserIdByUserName(user)
                    # user_id = mysql.selectUseridByUsername(user)
                    # print(user_id)
                    # print(user_id)
                        # 插入到得分表中
                    adduserscore_result = mysql.addUserScore(group_id,ctfType,ctf_id,user_id,score,date)
                    print(adduserscore_result)
                    if adduserscore_result==1:
                        return "1"
                    else:
                        return "0"
                else:
                    return "0"
            else:
                return "0"
        else:
            return "0"
    else:
        return "0"




@app.route("/adminlogin")
def adminlogin():
    if session.get("admin"):
        return render_template("admin/login.html")
    return render_template('admin/login.html')


@app.route("/admin_notice")
def admin_notice():
    if session.get("admin"):
        selectUserNotice = Mysqld()
        userNotice = selectUserNotice.selectUserNotice()
        return render_template("admin/admin_notice.html",userNotice=userNotice)
    return render_template('admin/login.html')


# 检查admin登录情况
@app.route("/checkAdminLogin",methods=["POST"])
def checkAdminLogin():
    if session.get("admin"):
        return render_template("admin/index.html")
    if request.method == 'GET':
        #如果是GET方法请求的，那么重新登录
        return render_template('admin/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '' or password == '':  # 检查用户名和密码是否为空
            return render_template("admin/login.html", message="用户名或密码不能为空")
        checkuser = Mysqld()
        result = checkuser.checkAdminLogin(username, password)  # 对用户表进行操作，检查登录
        if result == 1:
            session.permanent = True  # 设置session为永久的
            app.permanent_session_lifetime = timedelta(minutes=20)  # 设置session到期时间，单位分钟
            session['admin'] = request.form.get('username')
            return redirect('/admin')
        else:
            return render_template("admin/login.html", message="帐号或密码错误")
    else:
        return redirect('/login')



# ============================后台=================================


# 后台首页
@app.route("/admin")
def adminIndex():
    admin = session.get('admin')
    if admin:
        return render_template("admin/index.html")
    else:
        return render_template("admin/login.html")



# 添加管理员
@app.route("/add_admin")
@app.route("/add_admin",methods=['POST'])
def add_admin():
    admin = session.get('admin')
    if admin:
        if request.method != 'POST':
            return render_template("admin/addAdmin.html")
        elif request.method == 'POST':
            name = request.form.get('name')
            passwd  = request.form.get('passwd')
            email = request.form.get('email')
            mobile = request.form.get('mobile')
            addAdmin = Mysqld()
            result  = addAdmin.addAdmin(name,email,mobile,passwd)
            if result:
                return render_template("admin/man_admin.html",message="成功添加记录")
        return  render_template("admin/addAdmin.html")
    else:
        return render_template("admin/login.html")




# upload_ctf_contain
@app.route("/upload_ctf_contain")
def upload_ctf_contain():
    admin = session.get('admin')
    if admin:
        return render_template("admin/upload_ctf.html")
    else:
        return render_template("admin/login.html")



@app.route("/upload_awd_contain")
def upload_awd_contain():
    admin = session.get('admin')
    if admin:
        return render_template("admin/upload_awd.html")
    else:
        return render_template("admin/login.html")




# CTF实例
@app.route("/man_ctf_instance")
def man_target_ctf():
    admin = session.get('admin')
    if admin:
        connectsql = Mysqld()
        ctfList  = connectsql.selectCtfInstanceList()
        print(ctfList)
        return render_template("admin/man_ctf_instance.html", ctfList=ctfList)
    else:
        return render_template("admin/login.html")
# man_target_awd
@app.route("/man_target_awd")
def man_target_awd():
    return render_template("admin/man_target_awd.html")

# CTF题目列表
@app.route("/man_ctf_exam")
def man_ctf_exam():
    admin = session.get('admin')
    if admin:
        mysql = Mysqld()
        ctf_exam = mysql.selectctf_exam()
        return render_template("admin/man_ctf_exam.html",ctf_exam=ctf_exam)
    else:
        return render_template("admin/login.html")


# CTF操作
# 添加CTF题目
# {#own_id,type,name,hint,base_score,status,flag_type,base_flag,file_flag,file_path,docker_flag,docker_path,info#}
@app.route("/man_ctf_add_exam",methods=["POST","GET"])
def man_ctf_add_exam():
    admin = session.get('admin')
    if admin:
        if request.method == 'POST':
            type = int(request.form.get('exam_type'))
            name = request.form.get('exam_name')
            hint = request.form.get('exam_hint')
            score = int(request.form.get("base_score"))
            # status = int(request.form.get('status'))
            flag = request.form.get('flag')
            flag_type = int(request.form.get('flag_type'))
            file_path = request.files['file']
            docker_file  = request.files['docker_file']
            info = request.form.get('info')
            createtime =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("000000000000000000000")
            print(file_path.filename)
            print(docker_file.filename)
            if file_path.filename == '':
                file_flag = 0
            else:
                file_flag = 1
                file_path.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_path.filename)))
            if docker_file.filename == '':
                docker_flag = 0
            else:
                docker_flag = 1
                docker_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(docker_file.filename)))

            # print(request.method)
            #先将文件保存到服务器然后再将文件路径上传到数据库
            mysql = Mysqld()
            own_id = mysql.selectAdminIdByAdminName(admin)
            result = mysql.addUserCtfExam(own_id,type,name,hint,score,0,flag_type,flag,file_flag,file_path.filename,docker_flag,docker_file.filename,info)
            if result == 1:
                return redirect(url_for('man_ctf_exam',message="添加成功")) #页面跳转
            else:
                return render_template("admin/man_ctf_add_exam.html",message="添加失败")
        else:
            # print(own_id)
            return render_template("admin/man_ctf_add_exam.html")
    else:
        return render_template("admin/login.html")


# @app.route('/upload')
# def upload_file():
#    return render_template('user/test.html')
# @app.route('/uploader', methods = ['GET', 'POST'])
# def uploader():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
#       return 'file uploaded success'


# 创建CTF实例
#通过ajax实现,所以返回类型一定要是字符串
# 如果是静态flag的话，只需要创建一个实例为所有队伍使用就行
@app.route("/create_ctf_instance",methods=['POST'])
def create_ctf_instance():
    admin = session.get('admin')
    if admin:
        ctf_exam_id = int(request.form.get('ctf_exam_id'))

        mysql  = Mysqld()
        ctf_exam_info = mysql.selectctf_examByctf_exam_Id(ctf_exam_id)
        if ctf_exam_info[6] == 0:  #[6]为flag类型为静态flag
            result  = mysql.add_user_challenge_list(0,ctf_exam_id)
            if result == 1:
                return "1"
            else:
                print("create_ctf_instance函数插入错误!")
                return "0"
    else:
        return "0"

# ajax实现
# 用来删除CTF题目
@app.route('/delete_ctf_exam',methods=["POST"])
def delete_ctf_exam():
    admin = session.get('admin')
    if admin:
        ctf_exam_id = int(request.form.get('ctf_exam_id'))
        mysql = Mysqld()
        result = mysql.delUserCtfExam(ctf_exam_id)
        if result == 1:
            return "1"
        else:
            return "0"
    else:
        print("未授权访问/delete_ctf_exam！")
        return "0"

# delete_ctf_instance
# ajax实现
# 用来删除CTF题目实例
@app.route('/delete_ctf_instance',methods=["POST"])
def delete_ctf_instance():
    admin = session.get('admin')
    if admin:
        id = int(request.form.get('id'))
        print(id)
        mysql = Mysqld()
        result = mysql.delUserCtfInstanceById(id)
        if result == 1:
            return "1"
        else:
            return "0"
    else:
        print("未授权访问/delete_ctf_exam！")
        return "0"


@app.route("/man_user")
def man_user():
    manAdmin = Mysqld()
    userList = manAdmin.selectUserList()
    return render_template("admin/man_user.html",userList=userList)

@app.route("/man_admin")

def man_admin():
    manAdmin = Mysqld()
    adminList = manAdmin.selectAdminList()
    if adminList:
        return render_template("admin/man_admin.html",adminList=adminList)
    return "404"

#管理员登录退出
@app.route("/adminLogout")
def adminLogout():
    session.clear()
    return render_template("admin/login.html",message="退出帐号成功，请重新登录")


# 靶场导入
@app.route("/run_target_import")
def run_target_import():
    admin = session.get('admin')
    if admin:
        return render_template("admin/run_target_import.html")
    else:
        return render_template("admin/login.html")



# run_target_table
@app.route("/run_target_table")
def run_target_table():
    admin = session.get('admin')
    if admin:
        return render_template("admin/run_target_table.html")
    else:
        return render_template("admin/login.html")


#==================404=====================

# 404错误
@app.errorhandler(404)
def page_not_found(error):
    user = session.get('user')
    if user:
        return render_template("404.html",username=user), 404
    return render_template("404.html"),404





# ===============函数====================


# 没啥用测试用的
# @app.route("/test")
# @app.route("/test",methods=["POST"])
# def test():
#     if request.method == 'POST':
#         f = request.files['file']
#         basepath = os.path.dirname(__file__)  # 当前文件所在路径
#         upload_path = os.path.join(basepath,'static\uploads',secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
#         f.save(upload_path)
#         return redirect(url_for('upload'))
#     return render_template('upload.html')

@app.route('/upload')
def upload_file():
   return render_template('user/test.html')
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
      return 'file uploaded success'




# 创建队伍
@app.route("/create_group",methods=['POST'])
def create_group():
    user = session.get('user')
    if user:
        groupName = request.form.get('groupname')
        groupInfo = request.form.get('groupinfo')
        mysql = Mysqld()
        userId = mysql.selectUserIdByUserName(user)
        if userId:
            addgroup = mysql.addGroup(groupName, groupInfo)
            if addgroup == 1:
                groupinfo = mysql.selectGrouInfoByGroupName(groupName)
                print(groupinfo)
                group_id = groupinfo[0]
                print(group_id)
                print(userId)
                if group_id != 0:
                    print("id:",end='')
                    # print(groupid)
                    addusergrouplistResult = mysql.addUser_group_list(group_id,userId,1)
                    if addusergrouplistResult==1:
                        return "1"
                    else:
                        return "0"
                else:
                    return "0"
            else:
                return "0"
        else:
            return "0"
    else:
        return "0"


if __name__ == '__main__':
    app.run()





