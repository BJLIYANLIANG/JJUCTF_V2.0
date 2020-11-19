from flask import Flask
from flask import render_template
from  flask import request
from  flask import session,redirect

app = Flask(__name__)
app.secret_key = '905008'  #session key
app.debug = True



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if request.form.get('username') == 'hsm':
            session['user'] = request.form.get('username')
            # session['user']
            result  = "登录成功"
            return redirect('/',)
        else:
            return redirect('/login')
    else:
        return redirect('/login')

#git
@app.route('/')
def index():
    user = session.get('user')
    if user :  #如果登录成功
        return render_template('index.html',name=user)
    return render_template('login.html')

if __name__ == '__main__':
    app.run()

