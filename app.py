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
        result = checkuser.checkUser(username,password)  #对用户表进行操作，检查登录
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
    if request.method != 'POST':
        return render_template("user/register.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        useremail = request.form.get('email')
        print(useremail,password,useremail)
        # if useremail=='' or password == '' or useremail == '':
        #     return render_template("")
        checkstr = Checkinnput()
        result = checkstr.checkUserString(username=username,password=password,useremail=useremail)  #检查用户输入的字符串
        if result == 0 :
            return render_template("user/register.html",message="提交异常，请重新输入")
        adduser = Mysqld()
        if adduser.checkUserRegister(username=username) == 1:
            return render_template("user/register.html",message="用户已经注册过!")

        result = adduser.addUser(userName=username,userEmail=useremail,userPassword=password)
        if result == 1:
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



if __name__ == '__main__':
    app.run()


