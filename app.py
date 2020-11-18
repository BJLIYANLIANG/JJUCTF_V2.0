from flask import Flask
from classContain.Contain import *
from flask import render_template
from  flask import request
app = Flask(__name__)
from flask import make_response


@app.route('/')
def index():
    resp = make_response(render_template("index.html"))
    resp.set_cookie('s','d')
    return resp
# @app.route('/')
# def hello_world():
#     aaa = Contain("hello world")
#     # print(aaa)
#     bbb = aaa.printA()
#     return str(bbb)
#
# def valid_login():
#     pass
#     return True
# def log_the_user_in():
#     return True
# @app.route('/login',methods=['POST','GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],request.form['password']):
#             return log_the_user_in(request.form['username'])
#     return render_template('login.html')
#
#
# @app.route('/user/hsm')
# def show_user_profile(username):
#     # show the user profile for that user
#     return ('User {0}'.format(1))
#
#
#
# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id
#
# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('index.html',name=name)

if __name__ == '__main__':
    # a = Contain(1)
    # print(a)
    app.run()

