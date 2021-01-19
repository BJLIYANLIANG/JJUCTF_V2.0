from flask import Flask,url_for,send_from_directory,render_template,abort,request,make_response
from flask import session,redirect,Response
from datetime import timedelta
import hashlib
import zipfile
import shutil
from jjuctf.man_Sql import Mysqld
from werkzeug.utils import secure_filename
import os
from flask_socketio import SocketIO,emit,join_room,leave_room,send
import redis
from jjuctf.config import *
from jjuctf.Check import Check
import time
from jjuctf.Crypto_AES import *
import datetime
from jjuctf.Contain import Contain

redis_instance = redis.Redis(host=redis_address, port=redis_port, decode_responses=True)

app = Flask(__name__)
app.secret_key = '905008'  #session 密钥
# app.debug = True
socketio = SocketIO(app,cors_allowed_origins='*')
# 没啥用测试用的
@socketio.on('test')
def test123():
    print('hello world')

@app.route("/test")
@app.route("/test",methods=["POST","GET"])
def test():
    return render_template("user/test.html")

@app.route('/push')
def push():
    event_name = 'test'
    broadcast_data = "hello world!"
    emit(event_name,broadcast_data,broadcast=True,namespace=name_space)
    return "done!"


name_space = '/test'
@socketio.on('connect',namespace=name_space)
def connected_msg():
    print('client connected.')

@socketio.on('disconnect',namespace=name_space)
def disconnect_msg():
    print('client disconnected.')


# 常量
app.config['UPLOAD_FOLDER'] = 'jjuctf/upload_file/'
app.config['UPLOAD_CTF_FILE'] = 'jjuctf/CTF_FILE/'
app.config['UPLOAD_CTF_CONTAINER'] = 'jjuctf/CTF_CONTAINER/'


@app.route('/login',methods=['GET','POST'])
def login():
    if session.get("user"):
        return render_template("user/index.html")
    if request.method == 'GET':
        return render_template('user/login.html')
    if request.method == 'POST':
        check = Check()
        username = request.form.get('username')
        password = request.form.get('password')
        if check.checksqlSecure(username)==0 or check.checksqlSecure(password)==0:
            return render_template("user/login.html",message="请勿攻击靶场，违者做违规处理！")
        if username == '' or password == '':  #检查用户名和密码是否为空
            return render_template("user/login.html",message="用户名或密码不能为空")
        mysql = Mysqld()
        group_id = mysql.selectGroupidByusername(username)
        result = mysql.checkuser(username,password) #对用户表进行操作，检查登录
        if result == 1:
            session.permanent = True  #设置session为永久的
            # app.permanent_session_lifetime = timedelta(minutes=20)  # 设置session到期时间，单位分钟
            session['user'] = request.form.get('username')
            resp = make_response(redirect(url_for('index')))
            message = str(group_id)+':'+username
            token = encrypt(message)
            print(token)
            # 添加token信息
            resp.set_cookie('token', token)
            return resp
        else:
            return render_template("user/login.html",message="帐号或密码错误")
    else:
        return redirect('/login')


# ctf解题模式
@app.route('/challenges')
def challenge():
    user = session.get('user')
    if user :  #如果登录成功
        #获取CTf实例列表
        check = Check()
        mysql = Mysqld()
        challengeResult = mysql.selectChallengeListByUserName(user)
        print(challengeResult)
        challengeNum = mysql.showChallengeNum()
        # challengeTypeNum = getChallengeListByType.selectCtfChallengeTypeNum(user)   #用这个代替上面那个！今天不写了，难受，我写的垃圾代码。。。
        groupInfo = mysql.selectGroupInfoByUsername(user)
        UserTypeNum = mysql.selectCtfTypeNum()
        # 如果该用户没有创建队伍，那么跳转让他创建队伍
        if groupInfo == 0:
            return redirect('/group')
        # 检查时候有token，如果没有，那么创建token
        # if request.cookies.get('token') is None:
        #     resp = make_response(redirect(url_for('challenges')))
        #     group_id = mysql.selectGroupidByusername(user)
        #     message = str(group_id) + ':' + user
        #     token = encrypt(message)
        #     print(token)
        #         # 添加token信息
        #     resp.set_cookie('token', token)
        #     return resp
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
        #转换为js需要的格式
        userChallengeinfo = mysql.selectUserChallengeListDesc()
        print(userChallengeinfo)
        startDateTime = str(competition_info[3])
        endDateTime = str(competition_info[4])
        end_time = str(competition_info[4]).replace('-','/')
        # 比赛状态码 如果比赛正在进行，则结果为1,已结束为2,未开始为0
        competition_StatusCode = check.checkCompetition_start(startDateTime,endDateTime)
        # print('conpetitioncode')
        # print(competition_StatusCode)
        userNotice = mysql.selectUserNotice()
        # print(userNotice)
        # 解题动态 CTF_History_table

        ctf_history_table = mysql.selectCtfHistoryTable()
        # 0为web 以此类推
        return render_template("user/challenge.html",username=user,headerType="challenges",challengeResult=challengeResult,ctf_history_table=ctf_history_table,examNum=challengeNum,groupInfo=groupInfo,userNotic=userNotice,competition_info=competition_info,end_time=end_time,competition_StatusCode=competition_StatusCode,UserTypeNum=UserTypeNum)
    return render_template('user/login.html')


# index
# ctf解题模式
@app.route('/')
@app.route('/index')
def index():
    user = session.get('user')
    if user :  #如果登录成功
        mysql = Mysqld()
        # 比赛信息
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
        return render_template("user/index.html",username=user,headerType="index",competition_info=competition_info)
    return render_template('user/login.html')





@app.route('/ranks')
def ranks():
    user = session.get('user')
    if user:
        mysql = Mysqld()
        #这个函数貌似没啥用了，有时间的话就把这个删除
        # GetChallengeList = mysql.select_user_challenge_list()
        # GetGroupInfo  = sqlcheck.
        getUserCTFChallengeList = mysql.selectUserChallengeListDesc()
        getUserCTFChallengeListNum = len(getUserCTFChallengeList)
        GetUserNum = mysql.selectUserNum(user)  #查数据库将排行榜数据传到template中，目前是测试阶段，使用的是用户表
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
        return render_template("user/ranks.html",username=user,headerType="rank",userNum=GetUserNum,a=1,getUserCTFChallengeList=getUserCTFChallengeList,getUserCTFChallengeListNum=getUserCTFChallengeListNum,competition_info=competition_info)
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
    resp = Response()
    if request.cookies.get('token'):
        resp.delete_cookie('token')
    resp.data = render_template("user/login.html",message="退出帐号成功，请重新登录")
    return resp



# AWD模块
@app.route('/awd')
def awd():
    user = session.get('user')
    if user:
        mysql = Mysqld()
        # 比赛信息
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
        return render_template("user/awd.html",username=user,headerType="awd",competition_info=competition_info)
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
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
        # print(userinfo)
        usergroupinfo = mysql.selectGroupInfoByUsername(user)
        # print(usergroupinfo)
        # print(usergroup)
        return render_template("user/user.html",username=username,headerType=username,userinfo=userinfo,usergroupinfo=usergroupinfo,competition_info=competition_info)
    else:
        return render_template("user/login.html")


# 队伍设置
@app.route('/group',methods=['GET'])
def groupSetting():
    user = session.get('user')
    if user:
        #获得用户名
        username = user
        mysql = Mysqld()
        # 得到用户信息
        userinfo = mysql.selectUserInfo(user)
        # 得到用户队伍的id，如果没有则为0
        group_id = mysql.selectGroupidByusername(user)
        # print(groupinfo)
        #得到比赛信息
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]


        # 如果存在比赛id
        if group_id!=0:
            groupinfo = mysql.selectGroupInfoByUsername(user)
            #队伍成员信息

            # 如果这个身份为队长，那么
            if groupinfo[3] == mysql.selectUserIdByUserName(user):
                UserApplyList = mysql.selectUserGroupApplyByGroupId(group_id)
            else:
                UserApplyList = ()


            userGroupList = mysql.selectUserGroupListByGroupId(group_id)
            #解题信息
            userScoreList = mysql.selectUserScoreListByGroupId(group_id)
            # print(userGroupList)
            # print(userScoreList)
            # (('hsm', 1),)
            # (('web1', 0, 'hsm', 100, datetime.datetime(2021, 1, 5, 11, 5, 43)),)
            # print(userinfo)
            return render_template("user/group.html",username=username,headerType="userSetting",userinfo=userinfo,group_id=group_id,groupinfo=groupinfo,userGroupList=userGroupList,competition_info=competition_info,userScoreList=userScoreList,UserApplyList=UserApplyList)
        else:
            return render_template("user/group.html",username=username,headerType="userSetting",competition_info=competition_info,userinfo=userinfo,group_id=group_id)

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
    challenge_id = int(request.form.get('ctf_id'))
    if user:
        if flag and challenge_id :
            # ctf_id就是CTF靶场id
                # 每创建一个题目都会创建一个或者多个ctf_id,静态flag只需要创建一个id即可
            a = Mysqld()
            result = a.checkFalg(flag, challenge_id)
            # result = 1
            #如果result为1则正确，0为不正确
            # print(result)
            if result == 1:  #查到flag正确
                mysql = Mysqld()
                group_id = mysql.selectGroupInfoByUsername(user)[0]
                groupname = mysql.selectGroupNameByGroupId(group_id)
                # print(group_id)
                if group_id != 0:
                    (ctfType,score) = mysql.selectCtfTypeAndScoreByChallenge_id(challenge_id)
                    # print(ctfType,score)
                    # date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    challenge_time = time.strftime("%H:%M:%S", time.localtime())
                    user_id = mysql.selectUserIdByUserName(user)
                    # 插入到得分表中
                    challengeinfo = mysql.selectChallengeInfoByChallengeId(challenge_id)
                    if challengeinfo:
                        # print(challengeinfo)
                        data = {'name': groupname, "target": challengeinfo[0], "date": challenge_time,"challenge_id":challenge_id,"score":str(score)}
                        # 广播战况
                        emit('challenge_list', data, broadcast=True,namespace='/challenges')
                        emit('group_message',data,room=str(group_id),namespace='/challenges')
                        print(str(group_id)+" :success track"+challengeinfo[0])
                    adduserscore_result = mysql.addUserScore(group_id,ctfType,challenge_id,user_id,score,challenge_time)
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

# ajax实现
@app.route("/delUserNotice",methods=["POST"])
def delUserNotice():
    if session.get('admin'):
        if request.method=='POST':
            id = int(request.form.get('id'))
            if id!=0:
                mysql = Mysqld()
                result = mysql.delUserNotice(id)
                if result==1:
                    return "1"
                else:
                    return "0"
            else:
                return "0"
    return "0"


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



# 管理员系统设置
@app.route("/setting_info")
def setting_info():
    admin = session.get("admin")
    admin_ip = request.remote_addr
    user_agent = request.user_agent
    if admin:
        return render_template("admin/setting_info.html",admin_ip=admin_ip,adminname=admin,user_agent=user_agent)
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
                return redirect(url_for('man_admin',message="成功添加记录"))
        return render_template("admin/addAdmin.html")
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
            try:
                type = int(request.form.get('exam_type'))
                flag_type = int(request.form.get('flag_type'))
                score = int(request.form.get("base_score"))
            except:
                return render_template("admin/man_ctf_add_exam.html", message="添加失败,请按规范输入！")
            name = request.form.get('exam_name')
            hint = request.form.get('exam_hint')
            flag = request.form.get('flag')
            #得到附件文件
            file_path = request.files['file']
            #得到docker-compose文件
            docker_file  = request.files['docker_file']
            #题目备注
            info = request.form.get('info')
            createtime =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(file_path.filename)
            print(docker_file.filename)
            if file_path.filename == '':
                #如果发现没有上传文件，则将flag标记为0，
                file_flag = 0
            else:
                file_flag = 1
                file_path.save(os.path.join(app.config['UPLOAD_CTF_FILE'], secure_filename(file_path.filename)))
            if docker_file.filename == '':
                docker_flag = 0
            else:
                # 上传docker zip包
                docker_flag = 1
                docker_file.save(os.path.join(app.config['UPLOAD_CTF_CONTAINER'], secure_filename(docker_file.filename)))
                # =======解压zip包=====
                print(app.config['UPLOAD_CTF_CONTAINER']+docker_file.filename)
                zip = zipfile.ZipFile(app.config['UPLOAD_CTF_CONTAINER']+docker_file.filename,'r')
                try:
                    zip.extractall(app.config['UPLOAD_CTF_CONTAINER'])
                except:
                    return render_template("admin/man_ctf_add_exam.html", message="添加CTF题目失败,解压失败！")
                zip.close()
                # == 解压缩完成 ==
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



# 创建CTF实例
#通过ajax实现,所以返回类型一定要是字符串
# 如果是静态flag的话，只需要创建一个实例为所有队伍使用就行
@app.route("/create_ctf_instance",methods=['POST'])
def create_ctf_instance():
    admin = session.get('admin')
    if admin:
        ctf_exam_id = int(request.form.get('ctf_exam_id'))
        mysql  = Mysqld()
        # 先检查是否已经创建过实例,实质是查challenge_list表是否存在数据
        checkinsert = mysql.checkCtf_exam_insertById(ctf_exam_id)
        if checkinsert == -1:
            return "-1"
        ctf_exam_info = mysql.selectctf_examByctf_exam_Id(ctf_exam_id)
        if ctf_exam_info[6] == 0:  #[6]为flag类型为静态flag
            result = mysql.add_user_challenge_list(0,ctf_exam_id)
            if result == 0:
                # return "1"
                print("create_ctf_instance函数插入错误!")
                return "0"

        # 创建Docker虚拟机
        if ctf_exam_info[11]==1:
            docker_name = ctf_exam_info[12]
            docker = docker = Contain()
            result = docker.startContain(docker_name)
            if result==0:
                return "0"
        return "1"
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
        # status[0],flag_type[1],file_flag[2],docker_flag[3],file_path[4],docker_path[5]
        ctf_exam_info = mysql.selectCtf_exam_DeleteInfoByCtf_exam_Id(ctf_exam_id)
        # 如果存在附件
        if ctf_exam_info[2] == 1:
            os.remove(app.config['UPLOAD_CTF_FILE']+ctf_exam_info[4])
        # 如果存在docker-compose文件
        if ctf_exam_info[3] == 1:
            shutil.rmtree(app.config['UPLOAD_CTF_CONTAINER']+ctf_exam_info[5][:-4])
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
    admin = session.get('admin')
    if admin:
        #消除意外弹框
        #启用之后，message参数将没用了
        # if request.args.get('message'):
        #     return redirect(url_for('man_user'))
        manAdmin = Mysqld()
        userList = manAdmin.selectUserList()
        return render_template("admin/man_user.html",userList=userList)
    else:
        return render_template("admin/login.html")



@app.route("/man_admin",methods=["GET"])
def man_admin():
    admin = session.get('admin')
    if admin:
        manAdmin = Mysqld()
        adminList = manAdmin.selectAdminList()
        if adminList:
            return render_template("admin/man_admin.html",adminList=adminList)
        return "404"
    else:
        return render_template('admin/login.html')

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


@app.route('/upload')
def upload_file():
   return render_template('user/upload.html')
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file1']
      print("request.url:"+str(request.url))
      print("success upload file:"+str(f.filename))
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
      return 'file uploaded success'
   else:
       return "500"


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
            addgroup = mysql.addGroup(groupName, groupInfo,userId)
            if addgroup == 1:
                groupinfo = mysql.selectGroupInfoByGroupName(groupName)
                # print(groupinfo)
                group_id = groupinfo[0]
                # print(group_id)
                # print(userId)
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
# 删除管理员用户
# Ajax实现
@app.route("/delete_admin",methods=["POST"])
def delete_admin():
    admin = session.get('admin')
    if admin:
        if request.method=="POST":
            admin_id = int(request.form.get('admin_id'))
            if admin_id:
                mysql = Mysqld()
                result = mysql.delAdminById(admin_id)
                if result==1:
                    return "1"
                else:
                    return "0"
            else:
                return "0"
    return "404"
@app.route("/delete_admin",methods=["POST"])
def disable_admin():
    admin = session.get('admin')
    if admin:
        if request.method=="POST":
            admin_id = int(request.form.get('admin_id'))
            if admin_id:
                mysql = Mysqld()
                result = mysql.disableAdminById(admin_id)
                if result==1:
                    return "1"
                else:
                    return "0"
            else:
                return "0"
    return "404"
# 获取用户管理员状态
@app.route("/changeAdminStatus",methods=["POST"])
def changeAdminStatus():
    admin = session.get('admin')
    if admin:
        if request.method == "POST":
            admin_id = int(request.form.get('admin_id'))
            if admin_id:
                mysql = Mysqld()
                result = mysql.changeAdminStatusById(admin_id)
                if result == 1:
                    return "1"
                else:
                    return "0"
            else:
                return "0"
    return "404"
@app.route("/man_ctf_exam_info")
def man_ctf_exam_info():
    admin = session.get("admin")
    if admin:
        mysql = Mysqld()
        userNum = len(mysql.selectUserList())
        groupNum = len(mysql.selectUserGroupList())
        # groupNum = len(mysql.selectUserGroupListByGroupId())
        # 用户挑战数的
        user_Challenge_List_Num = len(mysql.select_user_challenge_list())
        # 查找CTF解题情况
        user_succcess_challenge_list = mysql.selectUserChallengeList()
        return render_template("admin/man_ctf_exam_info.html",userNum=userNum,groupNum=groupNum,user_Challenge_List_Num=user_Challenge_List_Num,user_succcess_challenge_list=user_succcess_challenge_list)
    else:
        return render_template("admin/login.html")

# 管理用户
@app.route("/man_group")
def man_group():
    admin = session.get("admin")
    if admin:
        mysql = Mysqld()
        groupList = mysql.selectUserGroupList()
        return render_template("admin/man_group.html",groupList=groupList)
    else:
        return render_template("admin/login.html")

#删除队伍
#ajax
@app.route("/delUserGroup",methods=["POST"])
def delUserGroup():
    if session.get("admin"):
        if request.method=="POST":
            id = int(request.form.get('id'))
            mysql = Mysqld()
            rel = mysql.deluser_group_listByGroupId(id)
            if rel==1:
                result = mysql.delGroupByGroup_Id(id)
            else:
                result = 0
            if result==1:
                return "1"
            else:
                return "0"
        return "0"
    else:
        return "0"

@app.route("/manGroupInfo")
def manGroupInfo():
    if session.get("admin"):
        return render_template("admin/man_group_about_user.html")
    else:
        return render_template("admin/login.html")


@app.route("/competition")
def competition():
    admin = session.get("admin")
    id_str = request.args.get('id')
    try:
        id = int(id_str)
    except:
        return "参数错误!"
    if admin:
        mysql = Mysqld()
        result = mysql.selectCompetitionInfoListById(id)
        return render_template("admin/competition_info.html",competitionInfo=result,id=id)
    else:
        return render_template("admin/login.html")
# form表单实现
@app.route("/addUserNotice",methods=["POST"])
def addUserNotice():
    admin = session.get('admin')
    if admin:
        mysql = Mysqld()
        admin_id = mysql.selectAdminIdByAdminName(admin)
        info  = request.form.get('info')
        result = mysql.addUserNotice(admin_id,info)
        if result==1:
            return redirect(url_for('admin_notice',message="添加成功"))
            # return render_template("admin/.html",message="添加公告成功")
        else:
            return redirect(url_for('admin_notice', message="添加失败"))
            # return render_template("admin/admin_notice.html",message="添加失败!")
    else:
        return render_template("admin/login.html")
        # admin_id =
# @app.route('')
# n_id

# form表单实现
@app.route("/changeUserNotice",methods=["POST"])
def changeUserNotice():
    admin = session.get('admin')
    if admin:
        mysql = Mysqld()
        admin_id = mysql.selectAdminIdByAdminName(admin)
        id = int(request.form.get('n_id'))
        info  = request.form.get('info')
        result = mysql.changeUserNotice(id,admin_id,info)
        if result==-1:
            return redirect(url_for('admin_notice', message="修改失败!您输入的信息长度不足5个字符长度！请重新修改"))
        if result==1:
            return redirect(url_for('admin_notice',message="修改成功"))
        else:
            return redirect(url_for('admin_notice', message="修改失败"))
    else:
        return render_template("admin/login.html")


@app.route("/changeCompetitionInfo",methods=["POST"])
def changeCompetitionInfo():
    admin = session.get("admin")
    if admin:
        if request.method=="POST":
            id_str = request.form.get('id')
            print(id_str)
            try:
                # print("id:"+str(id))
                id = int(id_str)
            # except:
                # id = 0
            except:
                return redirect(url_for('admin_competition_list',message="修改失败！检测到特殊字符"))
            name = request.form.get('name')
            info = request.form.get('info')
            start_date = str(request.form.get('start_date')).replace('T',' ')+":00"
            end_date  = str(request.form.get('end_date')).replace('T',' ')+":00"
            # print(start_date)
            # print(end_date)
            start_time = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(end_date,"%Y-%m-%d %H:%M:%S")
            mysql = Mysqld()
            result = mysql.changeCompetitionInfo(name,info,start_time,end_time,id)
            if result==1:
                return redirect(url_for('admin_competition_list',message="修改成功！"))
            else:
                return redirect(url_for('admin_competition_list',message="修改失败！"))

    else:
        return render_template("admin/login.html")


@app.route("/delUser",methods=["POST","GET"])
def delUser():
    admin = session.get("admin")
    if admin:
        if request.method == "POST":
            id = int(request.form.get('id'))
            mysql = Mysqld()
            result = mysql.delUserByUserId(id)
            if result==1:
                return "1"
            else:
                return "0"
        else:
            return "0"
    return "0"



@app.route("/admin_notice_change")
def admin_notice_change():
    admin = session.get('admin')
    if admin:
        id = int(request.args.get('id'))
        mysql = Mysqld()
        notice = mysql.selectUserNoticeByid(id)
        return render_template('admin/admin_notice_change.html',notice=notice)

    else:
        return render_template('admin/login.html')
@app.route("/man_user_change")
def man_user_change():
    admin = session.get('admin')
    if admin:
        id = int(request.args.get('id'))
        mysql = Mysqld()
        # userinfo = mysql.
        userinfo = mysql.selectUserInfoById(id)
        print(userinfo)
        # notice = '123'
        return render_template('admin/man_user_change.html',userinfo=userinfo)
    else:
        return render_template('admin/login.html')

@app.route('/man_user_change_save',methods=["POST"])
def man_user_change_save():
    admin = session.get('admin')
    if admin:

        name = request.form.get('user_name')
        real_name = request.form.get('real_name')
        class_id = request.form.get('cid')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        # print(name,real_name,sid,email,mobile)
        mysql = Mysqld()
        id = mysql.selectUserIdByUserName(name)
        result = mysql.changeUserinfo(name,real_name,email,mobile,class_id,id)
        if result==1:
            return redirect(url_for('man_user',message="修改成功！"))
        else:
            return redirect(url_for('man_user',message="修改失败"))
    else:
        return redirect(url_for('man_user',message="修改失败"))
@app.route("/man_addUser",methods=["POST"])
def man_addUser():
    admin = session.get('admin')
    if admin:
        if request.method=="POST":
            name = request.form.get('user_name')
            email = request.form.get('email')
            passwd1 = request.form.get('passwd1')
            passwd2 = request.form.get('passwd2')
            if passwd1!=passwd2:
                return redirect(url_for('man_user', message="两次输入密码不相同!"))
            mysql = Mysqld()
            result = mysql.adduser(name,passwd1,email)
            if result==1:
                return redirect(url_for('man_user',message="添加成功！"))
            else:
               return redirect(url_for('man_user',message="添加失败！"))
    else:
        return render_template("admin/login.html")

# 下载文件
@app.route("/download/<path:filename>")

def downloader(filename):
    user = session.get('user')
    print(request.user_agent)
    print(user)
    if user:
         # dirpath = os.path.join(app.root_path, 'upload')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
        return send_from_directory(app.config['UPLOAD_CTF_FILE'], filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载
    else:
        return abort(404)

# ajax实现
@app.route("/delAllUserChallengeList",methods=["POST"])
def delAllUserChallengeList():
    user = session.get('admin')
    if user:
        key = int(request.form.get('key'))
        print(key)
        if key == 1:
            mysql = Mysqld()
            result = mysql.delAllUserChallengeList()
            if result ==1:
                return "1"
            else:
                return "0"
        else:
            return "0"
    else:
        return redirect(url_for('login'))

@app.route('/search_group',methods=["POST","GET"])
def search_group():
    user = session.get('user')
    if user:
        if request.method == "POST":
            group_name = request.form.get('groupname')
            mysql = Mysqld()
            mygroup_id = mysql.selectGroupInfoByUsername(user)
            if mygroup_id :
                if group_name == mygroup_id[1]:
                    # 不能加入自己的id
                    return "500"

            searchGroupResult = mysql.searchGroupListByGroupname(group_name)
            print(searchGroupResult)
            if searchGroupResult !=0 and searchGroupResult != -1:
                data ={'name':searchGroupResult[0],'id':searchGroupResult[3]}
                return data
            else:
                return "0"
        else:
            return "-1"
    else:
        return "检测到越权访问!"


@app.route('/push_ws')
def push_ws():
    date = {'name':"jjusec2","target":"web1","date":"2020"}
    emit('challenge_list',date,broadcast=True,namespace='/challenges')
    return 'done!'


# ajax实现用户申请
@app.route('/group_apply',methods=["POST"])
def group_apply():
    user = session.get('user')
    if user:
        group_id = int(request.form.get('id'))
        mysql = Mysqld()
        user_id = mysql.selectUserIdByUserName(user)
        checkapply = mysql.checkAddGroupApply(user_id,group_id)
        if checkapply:
            return "500"
        result = mysql.addUserGroupApply(user_id,group_id)
        if result == 1:
            return "1"
        else:
            return "0"
    else:
        return "0"



# 加入队伍组,/challenges上用的
@socketio.on("join_group",namespace='/challenges')
def on_join(data):
    token = data["token"]
    message = decrypt(token)
    arrmessage = message.split(':')
    group_id = arrmessage[0]
    username = arrmessage[1]
    # print(group_id)
    # print(username)
    join_room(group_id)
    print(f"client {username} wants to join: {group_id}")
    # emit("group_message",f"Welcome to {group_id}, {username}", room=group_id)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@app.route('/admin_competition_list')
def admin_competition_list():
    admin = session.get('admin')
    if admin:
        mysql = Mysqld()
        CompetitionList = mysql.selectCompetitionInfoList()
        return render_template('admin/competition_list.html',CompetitionList=CompetitionList)
    else:
        return render_template('admin/login.html')



# 用户使用的比赛列表
@app.route('/user_competition_list')
def user_competition_list():
    user = session.get('user')
    if user:
        mysql = Mysqld()
        competitionlist = mysql.selectCompetitionInfoList()
        print(competitionlist)
        return render_template('user/competition_list.html',competitionlist=competitionlist)
    else:
        # return render_template('user/login.html')
        return render_template('user/login.html')

if __name__ == '__main__':
    # app.run()
    socketio.run(app,host='0.0.0.0',port=5000,debug=True)



