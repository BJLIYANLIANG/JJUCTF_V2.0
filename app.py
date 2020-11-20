from flask import Flask
from flask import render_template
from  flask import request
from  flask import session,redirect,escape
from datetime import timedelta
from jjuctf.mysqld import Mysqld
from jjuctf.Checkinput import Checkinnput
app = Flask(__name__)
app.secret_key = '905008'  #session 密钥
app.debug = True


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
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


            return redirect('/user/index')
        else:
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        useremail = request.form.get('email')
        Checkinnput.checkUserString(username=username,password=password,useremail=useremail)  #检查用户输入的字符串
        adduser = Mysqld()
        if adduser.checkUserRegister(username=username) == 1:
            return render_template("register.html",message="用户已经注册过!")

        result = adduser.addUser(userName=username,userEmail=useremail,userPassword=password)
        if result == 1:
            return render_template("login.html",message="注册成功！")
    return render_template("register.html")



@app.route('/')
def index():
    user = session.get('user')
    if user :  #如果登录成功
        return render_template('index.html',name=user)
    return render_template('login.html')

@app.route('/user/<path:index>')
def userIndex(index):
    user = session.get('user')
    if user :  #如果登录成功
        return render_template('user/index.html',name=user)
    return render_template('login.html')

@app.route('/user/<path:challenge>')
def challenge(challenge):
    user = session.get('user')
    # return "hello"
    if user:
        return render_template("user/challenge.html")
    return redirect('/')
    # return render_template("user/challenge.html")
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

if __name__ == '__main__':
    app.run()

