from flask import Flask, url_for, send_from_directory, render_template, abort, request, make_response, session, redirect, Response
from datetime import timedelta
import zipfile
import shutil
import sys
import logging
import jsonify
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import redis
import datetime
from jjuctf.config import *
from jjuctf.Check import *
from jjuctf.Crypto import *
from jjuctf.Container import *
from jjuctf.functions import *
import random
import json

# redis 连接
redis_instance = redis.Redis(host=redis_address, port=redis_port, decode_responses=True)

app = Flask(__name__)
app.secret_key = '905008'  # session 密钥
handler = logging.FileHandler('jjuctf.log')
app.logger.addHandler(handler)
socketio = SocketIO(app, cors_allowed_origins='*')


# 命名空间
name_space = '/test'

# 常量
app.config['UPLOAD_FOLDER'] = 'jjuctf/upload_file/'
app.config['UPLOAD_CTF_FILE'] = 'jjuctf/CTF_FILE/'
app.config['UPLOAD_CTF_CONTAINER'] = 'jjuctf/CTF_CONTAINER/'
app.config['UPLOAD_AWD_CONTAINER'] = 'jjuctf/AWD_CONTAINER/'



# 没啥用测试用的
@socketio.on('test')
def test123():
    print('hello world')


@app.route("/test")
@app.route("/test", methods=["POST", "GET"])
def test():
    return render_template("user/index_bak.html")


@app.route('/push')
def push():
    event_name = 'test'
    broadcast_data = "hello world!"
    emit(event_name, broadcast_data, broadcast=True, namespace=name_space)
    return "done!"

@socketio.on('connect', namespace=name_space)
def connected_msg():
    print('client connected.')


@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    print('client disconnected.')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("user"):
        return render_template("user/index.html")
    if request.method == 'GET':
        return render_template('user/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if check_input(username) == 0 or check_input(password) == 0:
            return render_template("user/login.html", message="请勿攻击靶场，违者做违规处理！")
        if username == '' or password == '':  # 检查用户名和密码是否为空
            return render_template("user/login.html", message="用户名或密码不能为空")
        mysql = Mysqld()
        # 查一下是否拥有队伍
        group_id = mysql.selectGroupidByusername(username)
        # 防止重复注册

        result = mysql.checkuser(username, password)  # 对用户表进行操作，检查登录
        # result为1表示该用户名未注册过
        if result == 1:
            session.permanent = False  # 设置session为永久的
            # app.permanent_session_lifetime = timedelta(minutes=20)  # 设置session到期时间，单位分钟
            session['user'] = request.form.get('username')
            if group_id != 0:
                resp = make_response(redirect(url_for('index')))
                # print(group_id)/
                message = str(group_id) + ':' + username
                # print(message)
                token = encrypt(message)
                # print(token)
                # 添加token信息
                resp.set_cookie('token', token)
                return resp
            else:
                return redirect(url_for('index'))
                # return render_template('user/index.html', message="登陆成功")
        else:
            return render_template("user/login.html", message="帐号或密码错误")
    else:
        return redirect('/login')



# ctf解题模式
@app.route('/challenges')
def challenge():
    app.logger.info("success")
    user = session.get('user')
    if user:  # 如果登录成功
        # 获取CTf实例列表
        check = Check()
        mysql = Mysqld()
        challengeResult = mysql.selectChallengeListByUserName(user)
        # print(challengeResult)
        # 展示题目列表
        challengeNum = mysql.showChallengeNum()
        # challengeTypeNum = getChallengeListByType.selectCtfChallengeTypeNum(user)   #用这个代替上面那个！今天不写了，难受，我写的垃圾代码。。。
        # 查找队伍信息
        groupInfo = mysql.selectGroupInfoByUsername(user)
        #
        UserTypeNum = mysql.selectCtfTypeNum()
        # 如果该用户没有创建队伍，那么跳转让他创建队伍
        if groupInfo == 0:
            return redirect('/group')
        challenge_list_rank = mysql.selectChallengeListRank()
        # 分别得到排名，分数，解题数
        rank, score, Challenge_Count = sortChallengeByGroupId(challenge_list_rank, groupInfo[0])
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
        # 转换为js需要的格式
        userChallengeinfo = mysql.selectUserChallengeListDesc()
        startDateTime = str(competition_info[3])
        endDateTime = str(competition_info[4])
        end_time = str(competition_info[4]).replace('-', '/')
        # 比赛状态码 如果比赛正在进行，则结果为1,已结束为2,未开始为0
        competition_StatusCode = check.checkCompetition_start(startDateTime, endDateTime)
        # 公告栏
        userNotice = mysql.selectUserNotice()
        # 解题动态 CTF_History_table
        ctf_history_table = mysql.selectCtfHistoryTable()

        # 0为web 以此类推
        return render_template("user/challenge.html", username=user, headerType="challenges",
                               challengeResult=challengeResult, ctf_history_table=ctf_history_table,
                               examNum=challengeNum, groupInfo=groupInfo, userNotice=userNotice,
                               competition_info=competition_info, end_time=end_time,
                               competition_StatusCode=competition_StatusCode, UserTypeNum=UserTypeNum,
                               rank=rank, sum_score=score, Challenge_Count=Challenge_Count)
    return render_template('user/login.html')


# 排序，找出带队伍的名次
def sortChallengeByGroupId(challenge_info, id):
    # 当没有解题信息的时候,就返回这个
    # rank,sls
    # core,Challenge_Count
    if challenge_info == ():
        return None, 0, 0
    rankid = 1
    for i in challenge_info:
        if id == i[0]:
            return rankid, i[1], i[2]
        else:
            rankid += 1
    return None, 0, 0


# index
# ctf解题模式
@app.route('/')
@app.route('/index')
def index():
    user = session.get('user')
    if user:  # 如果登录成功
        mysql = Mysqld()
        # 比赛信息
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
        return render_template("user/index.html", username=user, headerType="index", competition_info=competition_info)
    return render_template('user/login.html')


@app.route('/ranks')
def ranks():
    user = session.get('user')
    type = request.args.get('type')
    if user:
        mysql = Mysqld()
        # 这个函数貌似没啥用了，有时间的话就把这个删除
        # GetChallengeList = mysql.select_user_challenge_list()
        # GetGroupInfo  = sqlcheck.
        if type == 'ctf':
            getUserCTFChallengeList = mysql.selectUserChallengeListDesc()
            getUserCTFChallengeListNum = len(getUserCTFChallengeList)
            GetUserNum = mysql.selectUserNum(user)  # 查数据库将排行榜数据传到template中，目前是测试阶段，使用的是用户表
            competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
            return render_template("user/ranks-ctf.html", username=user, headerType="rank", userNum=GetUserNum, a=1,
                                   getUserCTFChallengeList=getUserCTFChallengeList,
                                   getUserCTFChallengeListNum=getUserCTFChallengeListNum,
                                   competition_info=competition_info)
        if type == 'awd':
            getUserAWDChallengeList = mysql.select_awd_rank_desc()
            getUserAWDChallengeListNum = len(getUserAWDChallengeList)
            GetUserNum = mysql.selectUserNum(user)  # 查数据库将排行榜数据传到template中，目前是测试阶段，使用的是用户表
            competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
            return render_template("user/ranks-awd.html", username=user, headerType="rank", userNum=GetUserNum, a=1,
                                   getUserAWDChallengeList=getUserAWDChallengeList,
                                   getUserAWDChallengeListNum=getUserAWDChallengeListNum,
                                   competition_info=competition_info)
        else:
            return render_template("404.html")

    else:
        return render_template("user/login.html")


@app.route('/register', methods=['POST', 'GET'])
def userRegister():
    if session.get('user'):
        return redirect(url_for('index',message='您已经登录，无需注册！'))
    if request.method != 'POST':  # 用户不是使用
        # =====start ====
        # 等号里面的代码可以随时删除
        # 思路：用于注册验证邮箱的，首先给注册者一个随机6位数，
        # 然后给注册者一个sesson，用于跟踪用户，
        # 然后注册者点击发送邮件，服务器就发送这个随机6位数给该邮箱
        # 当验证成功之后，就执行其他步骤。
        # 随机生产6位数字字符串
        serialMail = ''
        for i in range(6):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            serialMail += ch
        checkMailId = serialMail
        session['checkid'] = checkMailId
        print(checkMailId)
        # =====end =====
        return render_template("user/register.html")
    else:
        uid = request.form.get('uid')
        username = request.form.get('username')
        realname = request.form.get('realname')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        class_id = request.form.get('classid')
        passwd = request.form.get('passwd')

        resultEmpty = 0
        # result = checkstr.checkUserString(username=username,password=passwd,useremail=email,)  #检查用户输入的字符串
        if passwd == '' or username == '' or email == '' or mobile == '' or uid == '' or realname == '' or class_id == '':
            resultEmpty = 1

        if resultEmpty == 1:
            return render_template("user/register.html", message="提交异常，请重新输入")
        adduser = Mysqld()
        if adduser.checkUserRegister(username=username) == 1:
            return render_template("user/register.html", message="用户已经注册过!")
        result1 = adduser.adduser(username, passwd, email)
        if result1 == 1:
            return render_template("user/login.html", message="注册成功，请到队伍管理添加队伍！")



@app.route("/logout")
def logout():
    session.clear()
    resp = Response()
    if request.cookies.get('token'):
        resp.delete_cookie('token')
    resp.data = render_template("user/login.html", message="退出帐号成功，请重新登录")
    return resp


# AWD模块
@app.route('/awd')
def awd():
    user = session.get('user')
    if user:
        mysql = Mysqld()
        groupInfo = mysql.selectGroupInfoByUsername(user)
        # 如果该用户没有创建队伍，那么跳转让他创建队伍
        #
        if groupInfo == 0:
            return redirect('/group')
        # 比赛信息
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
        # 公告栏
        userNotice = mysql.selectUserNotice()
        # 挑战列表信息
        # (('test1234', 'awd_b4', '172.18.0.2', 0), ('admin', 'awd_b4', '172.18.0.3', 0))
        awd_target_list = mysql.select_awd_target_list()
        # awd挑战列表,最多有三个
        awd_list = mysql.select_awd_target_by_groupname(groupInfo[1])
        awd_rank_list = mysql.select_awd_rank_desc()
        return render_template("user/awd.html", username=user, headerType="awd", groupInfo=groupInfo,
                               competition_info=competition_info, userNotice=userNotice,awd_target_list=awd_target_list
                               ,awd_list=awd_list,awd_rank_list=awd_rank_list)
    else:
        return render_template("user/login.html")


# 用户个人设置
@app.route('/user', methods=['GET'])
def user():
    user = session.get('user')
    if user:
        username = user
        mysql = Mysqld()
        userinfo = mysql.selectUserInfo(user)
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
        # print(userinfo)
        usergroupinfo = mysql.selectGroupInfoByUsername(user)
        # print(usergroupinfo)
        # print(usergroup)
        return render_template('user/userinfo.html', username=username, headerType=username, userinfo=userinfo,
                               usergroupinfo=usergroupinfo, competition_info=competition_info)
        # return render_template("user/user.html", username=username, headerType=username, userinfo=userinfo,usergroupinfo=usergroupinfo, competition_info=competition_info)
    else:
        return render_template("user/login.html")


@app.route('/user_setting', methods=['GET'])
def user_setting():
    user = session.get('user')
    if user:
        mysql = Mysqld()
        userinfo = mysql.selectUserInfo(user)
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]
        usergroupinfo = mysql.selectGroupInfoByUsername(user)
        return render_template('user/user_setting.html', username=user, headerType=user,
                               competition_info=competition_info, userinfo=userinfo, usergroupinfo=usergroupinfo)
    else:
        return render_template('user/login.html')


# 队伍设置
@app.route('/group', methods=['GET'])
def groupSetting():
    user = session.get('user')
    if user:
        # 获得用户名
        username = user
        mysql = Mysqld()
        # 得到用户信息
        userinfo = mysql.selectUserInfo(user)
        # 得到用户队伍的id，如果没有则为0
        group_id = mysql.selectGroupidByusername(user)
        # print(groupinfo)
        # 得到比赛信息
        competition_info = mysql.selectCompetition_InfoByStatus(0)[0]

        # 如果存在比赛id
        if group_id != 0:
            groupinfo = mysql.selectGroupInfoByUsername(user)
            # 队伍成员信息

            # 如果这个身份为队长，那么
            if groupinfo[3] == mysql.selectUserIdByUserName(user):
                # uid形式表示
                applyList = mysql.selectUserGroupApplyByGroupId(group_id)
                UserApplyList = []
                # print(applyList)
                for uid in applyList:
                    list = []
                    applyUsername = mysql.selectUserNameByUserId(uid[0])
                    list.append(uid[0])
                    # print(applyUsername)
                    list.append(applyUsername)
                    UserApplyList.append(list)
                print(UserApplyList)
            else:
                UserApplyList = ()

            userGroupList = mysql.selectUserGroupListByGroupId(group_id)
            # 解题信息
            userScoreList = mysql.selectUserScoreListByGroupId(group_id)
            # print(userGroupList)
            # print(userScoreList)
            # (('hsm', 1),)
            # (('web1', 0, 'hsm', 100, datetime.datetime(2021, 1, 5, 11, 5, 43)),)
            # print(userinfo)
            return render_template("user/groupinfo.html", username=username, headerType="userSetting", userinfo=userinfo,
                                   group_id=group_id, groupinfo=groupinfo, userGroupList=userGroupList,
                                   competition_info=competition_info, userScoreList=userScoreList,
                                   UserApplyList=UserApplyList)
        else:
            return render_template("user/groupinfo.html", username=username, headerType="userSetting",
                                   competition_info=competition_info, userinfo=userinfo, group_id=group_id)

    else:
        return render_template("user/login.html")





# 检查CTF答题模式flag是否正确
# 通过ajax验证
@app.route("/checkCtfFlag", methods=["POST"])
def checkCtfFlag():
    # 检查flag需要ctf_id这个参数
    user = session.get("user")
    flag = request.form.get('flag')
    challenge_id = int(request.form.get('ctf_id'))
    if user:
        if flag and challenge_id:
            # ctf_id就是CTF靶场id
            # 每创建一个题目都会创建一个或者多个ctf_id,静态flag只需要创建一个id即可
            a = Mysqld()
            result = a.checkFalg(flag, challenge_id)
            # 如果result为1则正确，0为不正确
            # print(result)
            if result == 1:  # 查到flag正确
                mysql = Mysqld()
                group_id = mysql.selectGroupInfoByUsername(user)[0]
                groupname = mysql.selectGroupNameByGroupId(group_id)
                # 检查队伍之前是否提交过这个flag
                userPostFlag = mysql.checkUser_Post_Flag_OkByGroupIdAndCid(group_id, challenge_id)
                # print(group_id)
                # 如果返回值不为空,则表示之前已经提交过flag
                if userPostFlag:
                    return "501"
                # group_id!=0表示...
                if group_id != 0:
                    # 获取ctf类型和分数
                    (ctfType, score) = mysql.selectCtfTypeAndScoreByChallenge_id(challenge_id)
                    # 解答时间
                    challenge_time = time.strftime("%H:%M:%S", time.localtime())
                    # 用户id
                    user_id = mysql.selectUserIdByUserName(user)
                    # 插入到得分表中
                    challengeinfo = mysql.selectChallengeInfoByChallengeId(challenge_id)
                    if challengeinfo:
                        data = {'name': groupname, "target": challengeinfo[0], "date": challenge_time,
                                "challenge_id": challenge_id, "score": str(score)}
                        # 广播战况
                        emit('challenge_list', data, broadcast=True, namespace='/challenges')
                        # 更新队伍答题记录
                        adduserscore_result = mysql.addUserScore(group_id, ctfType, challenge_id, user_id, score,
                                                                 challenge_time)
                        ranknum = ctf_search_rank(groupname)
                        # print(ranknum)
                        data2 = {'name': groupname, "target": challengeinfo[0], "date": challenge_time,
                                "challenge_id": challenge_id, "score": str(score),"ranks":ranknum}
                        emit('group_message', data2, room=str(group_id), namespace='/challenges')
                        if adduserscore_result == 1:
                            return "1"
                        else:
                            return '0'
                    else:
                        return "0"
                else:
                    return "0"
            else:
                return "503"
        else:
            return "502"
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
        return render_template("admin/admin_notice.html", userNotice=userNotice)
    return render_template('admin/login.html')


# ajax实现
@app.route("/delUserNotice", methods=["POST"])
def delUserNotice():
    if session.get('admin'):
        if request.method == 'POST':
            id = int(request.form.get('id'))
            if id != 0:
                mysql = Mysqld()
                result = mysql.delUserNotice(id)
                if result == 1:
                    return "1"
                else:
                    return "0"
            else:
                return "0"
    return "0"


# 检查admin登录情况
@app.route("/checkAdminLogin", methods=["POST"])
def checkAdminLogin():
    if session.get("admin"):
        return render_template("admin/index.html")
    if request.method == 'GET':
        # 如果是GET方法请求的，那么重新登录
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
        mysql = Mysqld()
        userNum = len(mysql.selectUserList())
        groupNum = len(mysql.selectUserGroupList())
        # 用户挑战数的
        user_Challenge_List_Num = len(mysql.select_user_challenge_list())
        return render_template("admin/index.html",userNum=userNum,groupNum=groupNum,user_Challenge_List_Num=user_Challenge_List_Num)
    else:
        return render_template("admin/login.html")


# ajax
# /admin 里面的echart数据更新
@app.route('/get_ctf_type')
def get_ctf_type():
    admin = session.get('admin')
    if admin:
        typename = ['WEB', 'MISC', 'Crypto', 'Pwn', 'Reverse']
        mysql = Mysqld()
        ctf_type_num = mysql.select_ctf_type_num()
        for i in ctf_type_num:
            # web
            if i[0] == 0:
                web_num = i[1]
            if i[0] == 1:
                misc_num = i[1]
            if i[0] == 2:
                crypto_num = i[1]
            if i[0] == 3:
                reverse_num = i[1]
            if i[0] == 4:
                pwn_num = i[1]
        type_num = [{'value': web_num, 'name': 'WEB'},{'value': misc_num, 'name': 'MISC'},{'value': crypto_num, 'name': 'Crypto'},{'value': pwn_num, 'name': 'Pwn'},{'value': reverse_num, 'name': 'Reverse'}]
        return json.dumps({'typename':typename,'type_num':type_num},ensure_ascii=False)
    else:
        return ''



# 管理员系统设置
@app.route("/setting_info")
def setting_info():
    admin = session.get("admin")
    admin_ip = request.remote_addr
    user_agent = request.user_agent
    # 操作系统信息
    system_info = {}
    if os.name == 'nt':
        system_info['system_os'] = 'Windows'
    else:
        system_info['system_os'] = 'Linux'
    # python 版本

    python_version = sys.version
    system_info['python_version'] = python_version

    # 数据库版本

    mysql = Mysqld()
    sql_version = mysql.select_sql_version()
    system_info['sql_version'] = sql_version

    # docker版本

    docker = Contain()
    docker_version = docker.show_docker_version()
    system_info['docker_version'] = docker_version
    if admin:
        return render_template("admin/setting_info.html", admin_ip=admin_ip, adminname=admin, user_agent=user_agent,system_info=system_info)
    else:
        return render_template("admin/login.html")


# 添加管理员
@app.route("/add_admin")
@app.route("/add_admin", methods=['POST'])
def add_admin():
    admin = session.get('admin')
    if admin:
        if request.method != 'POST':
            return render_template("admin/addAdmin.html")
        elif request.method == 'POST':
            name = request.form.get('name')
            passwd = request.form.get('passwd')
            email = request.form.get('email')
            mobile = request.form.get('mobile')
            addAdmin = Mysqld()
            result = addAdmin.addAdmin(name, email, mobile, passwd)
            if result:
                return redirect(url_for('man_admin', message="成功添加记录"))
        return render_template("admin/addAdmin.html")
    else:
        return render_template("admin/login.html")


# CTF实例
@app.route("/man_ctf_instance")
def man_target_ctf():
    admin = session.get('admin')
    if admin:
        connectsql = Mysqld()
        ctfList = connectsql.selectCtfInstanceList()
        # print(ctfList)
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
        return render_template("admin/man_ctf_exam.html", ctf_exam=ctf_exam)
    else:
        return render_template("admin/login.html")


# CTF操作
# 添加CTF题目
# {#own_id,type,name,hint,base_score,status,flag_type,base_flag,file_flag,file_path,docker_flag,docker_path,info#}
@app.route("/man_ctf_add_exam", methods=["POST", "GET"])
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
            # 得到附件文件
            file_path = request.files['file']
            # file_path.save(os.path.join(app.config['UPLOAD_CTF_FILE'], secure_filename(file_path.filename)))
            # 得到docker-compose文件
            docker_file = request.files['docker_file']
            # 题目备注
            info = request.form.get('info')
            createtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            if file_path.filename == '':
                # 如果发现没有上传文件，则将flag标记为0，
                file_flag = 0
            else:
                file_flag = 1
                file_path.save(os.path.join(app.config['UPLOAD_CTF_FILE'], secure_filename(file_path.filename)))
            if docker_file.filename == '':
                docker_flag = 0
            else:
                # 上传docker zip包
                docker_flag = 1
                docker_file.save(
                    os.path.join(app.config['UPLOAD_CTF_CONTAINER'], secure_filename(docker_file.filename)))
                # =======解压zip包=====
                # print(app.config['UPLOAD_CTF_CONTAINER']+docker_file.filename)
                zip = zipfile.ZipFile(app.config['UPLOAD_CTF_CONTAINER'] + docker_file.filename, 'r')
                try:
                    zip.extractall(app.config['UPLOAD_CTF_CONTAINER'])
                except:
                    return render_template("admin/man_ctf_add_exam.html", message="添加CTF题目失败,解压失败！")
                zip.close()
                # == 解压缩完成 ==
                # 删除上传的zip包
                os.remove(app.config['UPLOAD_CTF_CONTAINER'] + docker_file.filename)
            mysql = Mysqld()
            own_id = mysql.selectAdminIdByAdminName(admin)
            result = mysql.addUserCtfExam(own_id, type, name, hint, score, 0, flag_type, flag, file_flag,
                                          file_path.filename, docker_flag, docker_file.filename, info)
            if result == 1:
                return redirect(url_for('man_ctf_exam', message="添加成功"))  # 页面跳转
            else:
                return render_template("admin/man_ctf_add_exam.html", message="添加失败")
        else:
            # print(own_id)
            return render_template("admin/man_ctf_add_exam.html")
    else:
        return render_template("admin/login.html")


# 创建CTF实例
# 通过ajax实现,所以返回类型一定要是字符串
# 如果是静态flag的话，只需要创建一个实例为所有队伍使用就行
@app.route("/create_ctf_instance", methods=['POST'])
def create_ctf_instance():
    admin = session.get('admin')
    if admin:
        ctf_exam_id = int(request.form.get('ctf_exam_id'))
        mysql = Mysqld()
        # 先检查是否已经创建过实例,实质是查challenge_list表是否存在数据
        checkinsert = mysql.checkCtf_exam_insertById(ctf_exam_id)
        # 查询这个实例之前是否创建过
        if checkinsert == -1:
            return "-1"
        ctf_exam_info = mysql.selectctf_examByctf_exam_Id(ctf_exam_id)
        # own_id = ctf_exam_info[1]
        type = ctf_exam_info[2]  # 题目类型 如web misc等
        name = ctf_exam_info[3]
        hint = ctf_exam_info[4]
        score = ctf_exam_info[5]
        flag = ctf_exam_info[7]
        file_flag = ctf_exam_info[8]
        file_info = ctf_exam_info[9]
        docker_flag = ctf_exam_info[10]
        docker_info = ctf_exam_info[11]
        # info = ctf_exam_info[13]
        # [6]为flag类型为静态flag
        if ctf_exam_info[6] == 0:
            # 如果docker_flag为1表示需要开启docker容器
            if ctf_exam_info[10] == 1:
                # 创建Docker虚拟机
                docker_name = ctf_exam_info[11]
                # print(docker_name)
                docker = Contain()
                # 打开虚拟机
                docker.startContain(docker_name)
                dockerid = docker.getDockerId(docker_name)
                # print(dockerid)
                docker_info = docker.geturl(dockerid)
            else:
                dockerid = [None]
            result = mysql.insertChallenge_list(0, ctf_exam_id, name, hint, score, type, docker_flag, dockerid[0],
                                                docker_info, file_flag, file_path=file_info, flag=flag)
            # result = mysql.add_user_challenge_list(0, ctf_exam_id)
            if result == 0:
                # return "1"
                print("create_ctf_instance函数插入错误!")
                return "0"
        # 动态flag:
        return "1"
    else:
        return "0"


# ajax实现
# 用来删除CTF题目
@app.route('/delete_ctf_exam', methods=["POST"])
def delete_ctf_exam():
    admin = session.get('admin')
    if admin:
        ctf_exam_id = int(request.form.get('ctf_exam_id'))
        mysql = Mysqld()
        # status[0],flag_type[1],file_flag[2],docker_flag[3],file_path[4],docker_path[5]
        ctf_exam_info = mysql.selectCtf_exam_DeleteInfoByCtf_exam_Id(ctf_exam_id)
        # 如果存在附件
        if ctf_exam_info[2] == 1:
            os.remove(app.config['UPLOAD_CTF_FILE'] + ctf_exam_info[4])
        # 如果存在docker-compose文件
        if ctf_exam_info[3] == 1:
            shutil.rmtree(app.config['UPLOAD_CTF_CONTAINER'] + ctf_exam_info[5][:-4])
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
@app.route('/delete_ctf_instance', methods=["POST"])
def delete_ctf_instance():
    admin = session.get('admin')
    if admin:
        id = int(request.form.get('id'))
        mysql = Mysqld()
        ctfinstanceinfo = mysql.selectInstanceDockerStatusByChallengeId(id)
        # group_id,docker_flag,ctf_exam_id
        # group_id为0表示为静态flag,只需要关闭
        if ctfinstanceinfo[0] == 0 and ctfinstanceinfo[1] == 1:
            dockerID = ctfinstanceinfo[3]
            # print(dockerID)
            dockerServer = Contain()
            dockerServer.stopContainByDockerID(dockerID)
        result = mysql.delUserCtfInstanceById(id)
        # result = 1
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
        # 消除意外弹框
        # 启用之后，message参数将没用了
        # if request.args.get('message'):
        #     return redirect(url_for('man_user'))
        manAdmin = Mysqld()
        userList = manAdmin.selectUserList()
        if userList:
            return render_template("admin/man_user.html", userList=userList)
        else:
            userList = ()
            return render_template("admin/man_user.html", userList=userList)
    else:
        return render_template("admin/login.html")


@app.route("/man_admin", methods=["GET"])
def man_admin():
    admin = session.get('admin')
    if admin:
        manAdmin = Mysqld()
        adminList = manAdmin.selectAdminList()
        if adminList:
            return render_template("admin/man_admin.html", adminList=adminList)
        return "404"
    else:
        return render_template('admin/login.html')

# 管理员登录退出
@app.route("/adminLogout")
def adminLogout():
    session.clear()
    return render_template("admin/login.html", message="退出帐号成功，请重新登录")




# 打开一个awd实例，必须知道images镜像id
@app.route("/start_awd_instance",methods=['GET','POST'])
def start_awd_instance():
    global data
    admin = session.get('admin')
    if admin:
        # 如果不是get请求
        if request.method == 'GET':
            redirect(url_for('man_awd_exam'))
        # image_id = '42941dbd1f82'
        image_id = request.form.get('image_id')
        docker = Contain()
        docker_status_code = docker.search_docker_image_in_system(image_id)
        if docker_status_code == -1:
            data = {'status': '20','message':'系统不存在该镜像！'}
            return data
        mysql = Mysqld()
        # 得到队伍信息
        # ((50, 'jjusec123'), (55, 'admin'))形式
        groupname_list = mysql.select_groupname()
        awd_info = mysql.select_awd_exam_by_imageID(image_id)
        # id,name,image_id,time,ssh,other_port
        ssh_user = awd_info[7]
        awd_name = awd_info[1]
        ssh_port = awd_info[4]
        other_port = awd_info[5]
        # 检查容器之前是否已经开启过
        open_status_code = mysql.get_awd_exam_open_status(awd_name)
        #
        if open_status_code == 1:
            data = {'status_code': '201', 'task_num': '1', 'task_total': '1','id': awd_name,'message':'该实例之前已经打开！'}
            emit('start_awd_exam', data, broadcast=True, namespace='/man_awd_exam')
            return '1'
        status = start_awd_instance_for(groupname_list,image_id,awd_name,ssh_port,other_port,ssh_user)
        print(status)
        if status == -1:
            data = {'status': '20','message':'容器启动错误！'}
        if status == 1:
            mysql.change_awd_exam_status_to_1_by_name(awd_name)
            data = {'status':'1'}
        return data
    else:
        return render_template("admin/login.html")


# 打开awd实例
def start_awd_instance_for(group_list, images_id, name, ssh_port, other_port, ssh_user):
    docker = Contain()
    mysql = Mysqld()
    now_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # print(now_time)
    # 得到ip
    task_num = 0
    task_total = len(group_list)
    try:
        # 初始化
        data = {'status_code': '200', 'task_num': str(task_num), 'task_total': task_total,'id': name}
        emit('start_awd_exam', data, broadcast=True, namespace='/man_awd_exam')
        task_num = 1
        for i in group_list:
            # 从ip池中获取一个ip
            ip = docker_get_ip()
            # print('image_id:',images_id)
            container_id = docker.docker_start_by_imagesID('tag', images_id, ip)
            # print('ip:',ip,'container_id:',container_id)
            if container_id == -1:
                data = {'status_code': '500', 'id': container_id, 'task_num': str(task_num - 1),'task_total': task_total, 'message': '启动镜像失败,image_id:'+images_id}
                emit('start_awd_exam', data, broadcast=True, namespace='/man_awd_exam')
                return -1
            print('启动容器成功', container_id)
            # 这里修改docker用户密码
            passwd = get_random_password(ssh_user)
            print('随机密码', passwd)
            result = docker.docker_change_passwd(container_id, ssh_user, passwd)
            if result == 1:
                print('修改密码成功', container_id)
            if result == -1:
                return -1
            status_code = mysql.insert_awd_instance(container_id, name, ssh_port, other_port, now_time, '', ip, 'tag',i[1], 1, ssh_user, passwd)
            if status_code == 0:
                data = {'status_code': '500', 'id': container_id, 'task_num': str(task_num-1), 'task_total': task_total,'message':'更新数据库错误'}
                emit('start_awd_exam', data, broadcast=True, namespace='/man_awd_exam')

            data = {'status_code':'200','task_num':str(task_num),'task_total':task_total,'id':name}
            emit('start_awd_exam', data, broadcast=True, namespace='/man_awd_exam')
            task_num += 1
        return 1
    except:
        return -1

# ==================404=====================
# 404错误
@app.errorhandler(404)
def page_not_found(error):
    user = session.get('user')
    if user:
        return render_template("404.html", username=user), 404
    return render_template("404.html"), 404


# ===============函数====================


@app.route('/upload')
def upload_file():
    return render_template('user/upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file1']
        # print("request.url:"+str(request.url))
        # print("success upload file:"+str(f.filename))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return 'file uploaded success'
    else:
        return "500"


# 创建队伍
@app.route("/create_group", methods=['POST'])
def create_group():
    user = session.get('user')
    if user:
        groupName = request.form.get('groupname')
        # 队伍名为空
        if groupName == '':
            # print("502")
            return "502"
        # 队伍名不能查过10字节
        if len(groupName) > 10:
            # print("501")
            return "501"
        groupInfo = request.form.get('groupinfo')
        mysql = Mysqld()
        userId = mysql.selectUserIdByUserName(user)
        if userId:
            addgroup = mysql.addGroup(groupName, groupInfo, userId)
            if addgroup == 1:
                groupinfo = mysql.selectGroupInfoByGroupName(groupName)
                group_id = groupinfo[0]
                if group_id != 0:
                    addusergrouplistResult = mysql.addUser_group_list(group_id, userId, 1)
                    if addusergrouplistResult == 1:
                        resp = make_response("1")
                        # print(group_id)/
                        message = str(group_id) + ':' + user
                        # print(message)
                        token = encrypt(message)
                        # 添加token信息
                        resp.set_cookie('token', token)
                        return resp
                        # return "1"
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
@app.route("/delete_admin", methods=["POST"])
def delete_admin():
    admin = session.get('admin')
    if admin:
        if request.method == "POST":
            admin_id = int(request.form.get('admin_id'))
            if admin_id:
                mysql = Mysqld()
                result = mysql.delAdminById(admin_id)
                if result == 1:
                    return "1"
                else:
                    return "0"
            else:
                return "0"
    return "404"


@app.route("/delete_admin", methods=["POST"])
def disable_admin():
    admin = session.get('admin')
    if admin:
        if request.method == "POST":
            admin_id = int(request.form.get('admin_id'))
            if admin_id:
                mysql = Mysqld()
                result = mysql.disableAdminById(admin_id)
                if result == 1:
                    return "1"
                else:
                    return "0"
            else:
                return "0"
    return "404"


# 获取用户管理员状态
@app.route("/changeAdminStatus", methods=["POST"])
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

        # groupNum = len(mysql.selectUserGroupListByGroupId())
        # 查找CTF解题情况
        user_succcess_challenge_list = mysql.selectUserChallengeList()
        return render_template("admin/man_ctf_exam_info.html",user_succcess_challenge_list=user_succcess_challenge_list)
    else:
        return render_template("admin/login.html")


# 管理用户
@app.route("/man_group")
def man_group():
    admin = session.get("admin")
    if admin:
        mysql = Mysqld()
        groupList = mysql.selectUserGroupList()
        return render_template("admin/man_group.html", groupList=groupList)
    else:
        return render_template("admin/login.html")


# 删除队伍
# ajax
@app.route("/delUserGroup", methods=["POST"])
def delUserGroup():
    if session.get("admin"):
        if request.method == "POST":
            # 获取队伍id
            id = int(request.form.get('id'))
            mysql = Mysqld()
            # 删除队伍里面的成员
            rel = mysql.deluser_group_listByGroupId(id)
            # print('rel',rel)
            if rel == 1:
                # 如果成功就再删除队伍
                result = mysql.delGroupByGroup_Id(id)
            else:
                result = 0
            if result == 1:
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
        return render_template("admin/competition_info.html", competitionInfo=result, id=id)
    else:
        return render_template("admin/login.html")


# form表单实现
@app.route("/addUserNotice", methods=["POST"])
def addUserNotice():
    admin = session.get('admin')
    if admin:
        mysql = Mysqld()
        admin_id = mysql.selectAdminIdByAdminName(admin)
        info = request.form.get('info')
        result = mysql.addUserNotice(admin_id, info)
        if result == 1:
            return redirect(url_for('admin_notice', message="添加成功"))
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
@app.route("/changeUserNotice", methods=["POST"])
def changeUserNotice():
    admin = session.get('admin')
    if admin:
        mysql = Mysqld()
        admin_id = mysql.selectAdminIdByAdminName(admin)
        id = int(request.form.get('n_id'))
        info = request.form.get('info')
        result = mysql.changeUserNotice(id, admin_id, info)
        if result == -1:
            return redirect(url_for('admin_notice', message="修改失败!您输入的信息长度不足5个字符长度！请重新修改"))
        if result == 1:
            return redirect(url_for('admin_notice', message="修改成功"))
        else:
            return redirect(url_for('admin_notice', message="修改失败"))
    else:
        return render_template("admin/login.html")


@app.route("/changeCompetitionInfo", methods=["POST"])
def changeCompetitionInfo():
    admin = session.get("admin")
    if admin:
        if request.method == "POST":
            id_str = request.form.get('id')
            # print(id_str)
            try:
                # print("id:"+str(id))
                id = int(id_str)
            # except:
            # id = 0
            except:
                return redirect(url_for('admin_competition_list', message="修改失败！检测到特殊字符"))
            name = request.form.get('name')
            info = request.form.get('info')
            start_time = str(request.form.get('start_date'))
            end_time = str(request.form.get('end_date'))
            if start_time == '' or end_time == '':
                return redirect(url_for('admin_competition_list', message="修改失败，未设置比赛时间！"))
            start_date = start_time.replace('T', ' ') + ":00"
            end_date = end_time.replace('T', ' ') + ":00"

            start_time = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            mysql = Mysqld()
            result = mysql.changeCompetitionInfo(name, info, start_time, end_time, id)
            if result == 1:
                return redirect(url_for('admin_competition_list', message="修改成功！"))
            else:
                return redirect(url_for('admin_competition_list', message="修改失败！"))

    else:
        return render_template("admin/login.html")


@app.route("/delUser", methods=["POST", "GET"])
def delUser():
    admin = session.get("admin")
    if admin:
        if request.method == "POST":
            uid = int(request.form.get('id'))
            # print(uid)
            mysql = Mysqld()
            group_id = mysql.selectGroupidByusername(uid)
            print(group_id)
            # 0 表示未加入队伍
            if group_id == 0:
                result = mysql.delUserByUserId(uid)
                if result == 1:
                    return "1"
                else:
                    return "0"
            else:
                return "1"
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
        return render_template('admin/admin_notice_change.html', notice=notice)

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
        # print(userinfo)
        # notice = '123'
        return render_template('admin/man_user_change.html', userinfo=userinfo)
    else:
        return render_template('admin/login.html')


@app.route('/man_user_change_save', methods=["POST"])
def man_user_change_save():
    admin = session.get('admin')
    if admin:
        name = request.form.get('user_name')
        real_name = request.form.get('real_name')
        class_id = request.form.get('cid')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        # print(name,real_name,sid,email,mobile)
        user_id = None
        mysql = Mysqld()
        id = mysql.selectUserIdByUserName(name)
        result = mysql.changeUserinfo(user_id,name, real_name, email, mobile, class_id, id)
        if result == 1:
            return redirect(url_for('man_user', message="修改成功！"))
        else:
            return redirect(url_for('man_user', message="修改失败"))
    else:
        return redirect(url_for('man_user', message="修改失败"))


@app.route("/man_addUser", methods=["POST"])
def man_addUser():
    admin = session.get('admin')
    if admin:
        if request.method == "POST":
            name = request.form.get('user_name')
            email = request.form.get('email')
            passwd1 = request.form.get('passwd1')
            passwd2 = request.form.get('passwd2')
            if passwd1 != passwd2:
                return redirect(url_for('man_user', message="两次输入密码不相同!"))
            mysql = Mysqld()
            result = mysql.adduser(name, passwd1, email)
            if result == 1:
                return redirect(url_for('man_user', message="添加成功！"))
            else:
                return redirect(url_for('man_user', message="添加失败！"))
    else:
        return render_template("admin/login.html")


# 下载文件
@app.route("/download/<path:filename>")
def downloader(filename):
    user = session.get('user')
    # print(request.user_agent)
    # print(user)
    if user:
        # dirpath = os.path.join(app.root_path, 'upload')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
        return send_from_directory(app.config['UPLOAD_CTF_FILE'], filename,
                                   as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载
    else:
        return abort(404)


# ajax实现
@app.route("/delAllUserChallengeList", methods=["POST"])
def delAllUserChallengeList():
    user = session.get('admin')
    if user:
        key = int(request.form.get('key'))
        # print(key)
        if key == 1:
            mysql = Mysqld()
            result = mysql.delAllUserChallengeList()
            if result == 1:
                return "1"
            else:
                return "0"
        else:
            return "0"
    else:
        return redirect(url_for('login'))


@app.route('/search_group', methods=["POST", "GET"])
def search_group():
    user = session.get('user')
    if user:
        if request.method == "POST":
            group_name = request.form.get('groupname')
            mysql = Mysqld()
            mygroup_id = mysql.selectGroupInfoByUsername(user)
            if mygroup_id:
                if group_name == mygroup_id[1]:
                    # 不能加入自己的id
                    return "500"

            searchGroupResult = mysql.searchGroupListByGroupname(group_name)
            # print(searchGroupResult)
            if searchGroupResult != 0 and searchGroupResult != -1:
                data = {'name': searchGroupResult[0], 'id': searchGroupResult[3]}
                return data
            else:
                return "0"
        else:
            return "-1"
    else:
        return "检测到越权访问!"


@app.route('/push_ws')
def push_ws():
    date = {'name': "jjusec2", "target": "web1", "date": "2020"}
    emit('challenge_list', date, broadcast=True, namespace='/challenges')
    return 'done!'


# ajax实现用户申请
@app.route('/group_apply', methods=["POST"])
def group_apply():
    user = session.get('user')
    if user:
        # 队伍id
        group_id = int(request.form.get('id'))
        mysql = Mysqld()
        # 查找这个用户的uid
        user_id = mysql.selectUserIdByUserName(user)
        # 检查这个用户想要申请的队伍之前是否加入过
        checkapply = mysql.checkAddGroupApply(user_id, group_id)
        # 如果加入过
        if checkapply:
            return "500"
        # 没有加入过的话,就让他加入到申请列表中
        result = mysql.addUserGroupApply(user_id, group_id)
        if result == 1:
            return "1"
        else:
            return "0"
    else:
        return "0"


# 加入队伍组,/challenges上用的
@socketio.on("join_group", namespace='/challenges')
def on_join(data):
    token = data["token"]
    print(token)
    if token:
        message = decrypt(token)
        # print(message)
        arrmessage = message.split(':')
        group_id = arrmessage[0]
        username = arrmessage[1]
        join_room(group_id)
        print(f"client {username} wants to join: {group_id}")
    else:
        return emit('timeout', broadcast=False)
    # emit("group_message",f"Welcome to {group_id}, {username}", room=group_id)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)


# 管理员用的比赛列表
@app.route('/admin_competition_list')
def admin_competition_list():
    admin = session.get('admin')
    if admin:
        mysql = Mysqld()
        CompetitionList = mysql.selectCompetitionInfoList()
        return render_template('admin/competition_list.html', CompetitionList=CompetitionList)
    else:
        return render_template('admin/login.html')


# 用户使用的比赛列表
@app.route('/user_competition_list')
def user_competition_list():
    user = session.get('user')
    if user:
        mysql = Mysqld()
        competitionlist = mysql.selectCompetitionInfoList()
        return render_template('user/competition_list.html', username=user,competitionlist=competitionlist)
    else:
        return render_template('user/login.html')



@app.route('/getChallengeTypeNum', methods=['POST'])
def getChallengeTypeNum():
    global miscNum, cryptoNum, reverseNum, webNum, pwnNum
    admin = session.get('admin')
    if admin:
        sqlServer = Mysqld()
        typeNum = sqlServer.select_challenge_list_Type_Count()
        for i in typeNum:
            if i[0] == 0:
                webNum = i[1]
                continue
            if i[0] == 1:
                miscNum = i[1]
                continue
            if i[0] == 2:
                cryptoNum = i[1]
                continue
            if i[0] == 3:
                reverseNum = i[1]
                continue
            if i[0] == 4:
                pwnNum = i[1]
            else:
                continue
        data = {'Web': webNum, 'Misc': miscNum, 'Crypto': cryptoNum, 'Reverse': reverseNum, 'Pwn': pwnNum}
        return jsonify
    else:
        return render_template('admin/login.html')


# 显示CTF实例细节
@app.route('/showCtfDetail')
def showCtfDetail():
    admin = session.get('admin')
    if admin:
        cid = request.args.get('id')
        if cid:
            id = int(cid)
            mysql = Mysqld()
            instanceinfo = mysql.selectCtfinstanceById(id)
            if instanceinfo != 0:
                return render_template('admin/man_ctf_instance_detail.html', instanceinfo=instanceinfo)
            else:
                pass
        else:
            return render_template('admin/man_ctf_instance.html')
    else:
        return render_template('admin/login.html')


# group.html用的
# 同意加入队伍申请
# ajax请求
@app.route('/great_apply', methods=['POST'])
def great_apply():
    username = session.get('user')
    if username:
        uid = int(request.form.get('uid'))

        if uid:
            # 首先将这个用户加入这个队伍
            # 然后在申请表中删除
            mysql = Mysqld()
            group_id = mysql.selectGroupidByusername(username)
            # 0表示队员
            code1 = mysql.addUser_group_list(group_id, uid, 0)
            code2 = mysql.delGroupApplyByUid(uid)
            if code1 == 1 and code2 == 1:
                return "200"
            else:
                return "502"
        else:
            # 表示没有uid这个参数
            return "501"
    else:
        return render_template('user/login.html')


@app.route('/modificationUserInfo', methods=['POST'])
def modificationUserInfo():
    user = session.get('user')
    if user:
        return "200"
    else:
        return render_template('user/login.html')


@app.route('/stopAllCTFInstance')
def stopAllCTFInstance():
    admin = session.get('admin')
    if admin:
        return "1"
    else:
        return render_template("admin/login.html")

@app.route('/index_ddw')
def index_ddw():
    username = session.get('user')
    if username:
        return render_template('user/index_bak.html')
    else:
        return render_template('user/login.html')


@app.route('/man_awd_exam',methods=['GET','POST'])
def man_awd_exam():
    admin = session.get('admin')
    if admin:
        # 上传题目
        if request.method == "POST":
            docker_name = request.form.get('docker_name')
            docker_file = request.files['zipfile']
            # 检查输入
            if docker_name == '':
                return render_template("admin/man_awd_exam.html", message="上传题目名字不能为空！")
            if docker_file == '':
                return render_template("admin/man_awd_exam.html", message="上传容器不能为空！")
            if docker_file.filename[-4:] != '.zip':
                return render_template("admin/man_awd_exam.html", message="上传容器一定要是zip压缩包格式！")
            mysql = Mysqld()
            file_hash = hash(docker_file.filename+docker_name)
            mysql.insert_awd_exam_table(docker_name,docker_file.filename[:-4],file_hash)
            docker_file.save(os.path.join(app.config['UPLOAD_AWD_CONTAINER'], secure_filename(docker_file.filename)))
            # =======解压zip包=====
            zip = zipfile.ZipFile(app.config['UPLOAD_AWD_CONTAINER'] + docker_file.filename, 'r')
            try:
                zip.extractall(app.config['UPLOAD_AWD_CONTAINER'])
                # 删除源文件
                os.remove(app.config['UPLOAD_AWD_CONTAINER'] + docker_file.filename)
            except:
                return render_template("admin/man_awd_exam.html", message="文件解压失败！")
            zip.close()
            # 构建镜像，并且将镜像id写入到题目中
            # mysql.insert_awd_exam_table(docker_name, docker_file.filename[:-4], file_hash)
            mysql.insert_awd_exam_table(docker_name, docker_file.filename[:-4], file_hash)
            return redirect(url_for('man_awd_exam',message="上传文件成功"))
        # GET请求
        else:
            mysql = Mysqld()
            awd_exam_table = mysql.select_awd_exam()
            # print(awd_exam_table)
            return render_template('admin/man_awd_exam.html',awd_exam_table=awd_exam_table)
    else:
        return render_template('admin/login.html')



@app.route('/man_awd_setting_config',methods=['POST','GET'])
def man_awd_setting_config():
    admin = session.get('admin')
    if admin:
        if request.method == 'POST':
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            score = int(request.form.get('score'))
            update_time = int(request.form.get('update_time'))
            check_time = int(request.form.get('check_time'))
            check_down_score = int(request.form.get('check_down_score'))
            salt = request.form.get('salt')
            mysql = Mysqld()
            result = mysql.awd_config_setting(start_time,end_time,update_time,check_time,score,check_down_score,salt)
            if result == 1:
                return redirect(url_for('man_awd_setting_config',message='修改成功'))
            else:
                return redirect(url_for('man_awd_setting_config', message='修改失败'))
        else:
            mysql = Mysqld()
            awd_config = mysql.select_awd_config()
            return render_template('admin/man_awd_setting_config.html',awd_config=awd_config)
    else:
        return render_template('admin/login.html')


@app.route('/man_awd_instance')
def man_awd_instance():
    admin = session.get('admin')
    if admin:
        mysql = Mysqld()
        awd_instance_list = mysql.select_awd_instance_list()
        return render_template('admin/man_awd_instance.html',awd_instance_list=awd_instance_list)
    else:
        return render_template('admin/login.html')

@app.route('/man_awd_instance_detail')
def man_awd_instance_detail():
    admin = session.get('admin')
    if admin:
        id = int(request.args.get('id'))
        if id:
            mysql = Mysqld()
            instance_detail = mysql.select_awd_instance_detail_by_id(id)
            print(instance_detail)
            if instance_detail:
                return  render_template('admin/man_awd_instance_detail.html',instance_detail=instance_detail)
    else:
        return  render_template('admin/login.html')


@app.route('/man_awd_exam_detail')
def man_awd_exam_detail():
    admin = session.get('admin')
    id_s = request.args.get('id')
    # return render_template('admin/man_awd_exam.html')
    if admin:
        try:
            id = int(id_s)
        except:
            id = ''
        if id:
            if id == 0:
                return redirect(url_for('man_awd_exam', message='请正确输入参数！'))
            else:
                mysql = Mysqld()
                awd_exam_detail = mysql.select_awd_exam_user_by_man_awd_exam_detail_by_id(id)
                print(awd_exam_detail)
                if awd_exam_detail is not None:
                    return  render_template('admin/man_awd_exam_detail.html',awd_exam_detail=awd_exam_detail)
                else:
                    return redirect(url_for('man_awd_exam',message='未找到内容！'))
        else:
            return redirect(url_for('man_awd_exam'))
    else:
        return  render_template('admin/login.html')



@app.route('/init_awd_score',methods=["POST"])
def init_awd_score():
    admin = session.get('admin')
    if admin:
        score_str = request.form.get('init_awd_score')
        score = int(score_str)
        status_code = init_awd_ranks(score)
        if status_code == 1:
            return redirect(url_for('man_awd_exam',message='初始化队伍分数成功！'))
        else:
            return redirect(url_for('man_awd_exam',message='初始化队伍分数失败！'))
    else:
        return render_template('admin/login.html')


# 关闭awd实例
# ajax
@app.route('/pl_stop_awd_instance',methods=['POST'])
def pl_stop_awd_instance():
    admin = session.get('admin')
    if admin:
        mysql = Mysqld()
        exam_name = request.form.get('name')
        print(exam_name)
        if exam_name:
            get_container_list = mysql.select_awd_exam_instance_container_id_by_exam_name(exam_name)
            docker = Contain()
            print(get_container_list)
            # 一个个关闭容器
            # container_id,ip
            for container in get_container_list:
                # 停止容器
                container_id = container[0]
                container_ip = container[1]
                code = docker.docker_stop_by_docker_id(container_id)
                if code !=1:
                    print('关闭实例失败',container_id)
                # 释放ip
                print('container_ip:',container_ip)
                docker_release_ip(container_ip)


            # 关闭之后更改状态码
            mysql.change_awd_exam_status_to_0_by_name(exam_name)

            # 更新数据库
            status_code = mysql.del_awd_instance_list_by_awdExamName(exam_name)
            if status_code != 1:
                return "501"
            return '200'
        else:
            return '502'
    else:
        return '503'



# 上传题目通过镜像id
@app.route('/post_exam_by_type_1', methods=['POST'])
def post_exam_by_type_1():
    admin = session.get('admin')
    if admin:
        exam_name = request.form.get('exam_name')
        docker_image_id = request.form.get('image_id')
        ssh_user = request.form.get('user')
        ssh_port_tmp = request.form.get('ssh_port')
        ssh_port = int(ssh_port_tmp)
        other_port_tmp = request.form.get('other_port')
        other_port = int(other_port_tmp)
        mysql = Mysqld()
        status_code = mysql.insert_awd_exam_table(exam_name,docker_image_id,ssh_user,ssh_port,other_port)
        if status_code == 1:
            return redirect(url_for('man_awd_exam',message='上传题目成功'))
        else:
            return redirect(url_for('man_awd_exam',message='上传题目失败！'))
    else:
        return render_template('admin/login.html')



# ajax
@app.route('/del_awd_exam_by_name',methods=["POST"])
def del_awd_exam_by_name():
    admin = session.get('admin')
    data = {}
    if admin:
        name = request.form.get('name')
        if name:
            mysql = Mysqld()
            awd_exam_open_status = mysql.get_awd_exam_open_status(name)
            if awd_exam_open_status == 1:
                data['message'] = '删除失败！请先停止AWD靶场实例！'
                data['code'] = '500'
                return data
            del_status_code = mysql.delete_awd_exam_by_exam_name(name)
            if del_status_code == 1:
                data['message'] = '删除成功！'
                data['code'] = '200'
                return data
            else:
                data['message'] = '删除失败！请检查参数是否正确！'
                data['code'] = '500'
                return data
        else:
            data['message'] = '删除失败！参数不能为空'
            data['code'] = '500'
            return data
    else:
        data['message'] = '未登录！'
        data['code'] = '500'
        return data



@app.route('/change_user_info',methods=['POST','GET'])
def change_user_info():
    user = session.get('user')
    if request.method == 'GET':
        return redirect(url_for('user'))
    if user:
        name = request.form.get('name')
        real_name = request.form.get('real_name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        class_name = request.form.get('class_name')
        # 学号
        user_id = request.form.get('user_id')
        mysql = Mysqld()
        id = mysql.selectUserIdByUserName(user)
        status_code = mysql.changeUserinfo(user_id,name,real_name,email,mobile,class_name,id)
        if status_code == 1:
            return redirect(url_for('user', message='用户修改成功'))
        else:
            return redirect(url_for('user', message='用户修改失败'))
    else:
        return redirect(url_for('user',message='用户修改失败'))



@app.route('/update_user_passwd',methods=['POST'])
def update_user_passwd():
    user = session.get('user')
    if user:
        mysql = Mysqld()
        uid = mysql.selectUserIdByUserName(user)
        old_pwd = request.form.get('old_pwd')
        new_pwd = request.form.get('pwd')
        if old_pwd =='' or new_pwd == '':
            return redirect(url_for('user', message='输入不能为空'))
        if check_input(old_pwd) != 1 or check_input(new_pwd) != 1:
            return redirect(url_for('user', message='输入信息潜在危险，已被拦截，请重新输入！'))
        status_code = mysql.update_user_passwd(uid,old_pwd,new_pwd)
        if status_code == 1:
            return redirect(url_for('user',message='密码修改成功'))

        else:
            return redirect(url_for('user',message='密码修改失败'))
    else:
        return redirect('login')



# 一定要放到最后
if __name__ == '__main__':
    # 初始化ip池
    init_ip_pool()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)