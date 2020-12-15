from flask import Flask
from flask import render_template
from  flask import request
from  flask import session,redirect
from datetime import timedelta
from jjuctf.mysqld import Mysqld
from jjuctf.Checkinput import Checkinnput
app = Flask(__name__)
app.secret_key = '905008'  #session 密钥
app.debug = True


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


@app.route('/ajax',methods=['POST'])
def ajax():
    return "1"


# ctf解题模式
@app.route('/challenges')
def challenge():
    user = session.get('user')
    if user :  #如果登录成功
        getChallenge_listByType = Mysqld()
        challengeResult = getChallenge_listByType.selectinfo(0)
        return render_template("user/challenge.html",username=user,headerType="challenge",challengeResult=challengeResult)
    return render_template('user/login.html')
# index
# ctf解题模式
@app.route('/')
@app.route('/index')
def index():
    user = session.get('user')
    if user :  #如果登录成功
        getChallenge_listByType = Mysqld()
        challengeResult = getChallenge_listByType.selectinfo(0)
        return render_template("user/index.html",username=user,challengeResult=challengeResult)
    return render_template('user/index.html',headerType="index")

@app.route('/ranks')
def ranks():
    user = session.get('user')
    if user:
        sqlcheck = Mysqld()
        GetChallengeList = sqlcheck.selectinfo(0)
        GetUserNum = sqlcheck.selectUserNum()  #查数据库将排行榜数据传到template中，目前是测试阶段，使用的是用户表
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
        result1 = adduser.adduser(uid,username,realname,passwd,email,mobile,int(class_id),'',0)
        if result1 == 1:
            return render_template("user/login.html",message="注册成功！")



@app.route("/logout")
def logout():
    session.clear()
    return render_template("user/login.html",message="退出帐号成功，请重新登录")



@app.route('/awd')
def awd():
    user = session.get('user')
    if user:
        return render_template("user/awd.html",username=user,headerType="awd")
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

@app.route("/checkflag",methods=["POST"])
def checkflag():
    return request.form.get("flag")




@app.route("/adminlogin")
def adminlogin():
    return render_template("admin/login.html")


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


@app.route("/admin")
def adminIndex():
    admin = session.get('admin')
    if admin:
        return render_template("admin/index.html")
    else:
        return render_template("admin/login.html")


@app.route("/userman")
def userman():
    return render_template("admin/useradmin.html")


# upload_ctf_contain
@app.route("/upload_ctf_contain")
def upload_ctf_contain():
    return render_template("admin/upload_ctf.html")

@app.route("/upload_awd_contain")
def upload_awd_contain():
    return render_template("admin/upload_awd.html")

# man_target_ctf
@app.route("/man_target_ctf")
def man_target_ctf():
    return render_template("admin/man_target_ctf.html")

# man_target_awd
@app.route("/man_target_awd")
def man_target_awd():
    return render_template("admin/man_target_awd.html")

@app.route("/man_user")
def man_user():
    return render_template("admin/man_user.html")

@app.route("/man_admin")
def man_admin():
    return render_template("admin/man_admin.html")


@app.route("/adminLogout")
def adminLogout():
    session.clear()
    return render_template("admin/login.html",message="退出帐号成功，请重新登录")

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


if __name__ == '__main__':
    app.run()




