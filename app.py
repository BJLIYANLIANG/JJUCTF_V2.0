from flask import Flask
from flask import render_template
from  flask import request
from  flask import session,redirect,escape
from datetime import timedelta
from jjuctf.mysqld import Mysqld
from flask import url_for
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
            return redirect('/', )
        checkuser = Mysqld()
        result = checkuser.checkUser(username,password)  #对用户表进行操作，检查登录
        if result == 1:
            session.permanent = True  #设置session为永久的
            app.permanent_session_lifetime = timedelta(minutes=20)  # 设置session到期时间，单位分钟
            session['user'] = request.form.get('username')


            return redirect('/')
        else:
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/ajax',methods=['POST'])
def ajax():
    return "hello world"



@app.route('/')
def userIndex():
    user = session.get('user')
    if user :  #如果登录成功
        return render_template("user/index.html",username=user)
    return render_template('user/login.html',username="11")


@app.route('/challenges')
def userchallenge(challenge):
    user = session.get('user')
    if user:
        return render_template("user/challenge.html")
    return redirect('/')


@app.route('/ranks')
def ranks():
    user = session.get('user')
    return render_template("user/ranks.html",username=user)


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
            print("111")
            return render_template("user/login.html",message="注册成功！")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("user/login.html",message="退出帐号成功，请重新登录")

@app.route("/settings")
def setting():
    return render_template("user/index.html")


if __name__ == '__main__':
    app.run()

