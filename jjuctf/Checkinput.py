from flask import render_template
class Checkinnput:
    def __init__(self):
        pass
    def checkUserString(self,username,password,useremail):
        if username == '' or password == '' or useremail == '':
            return render_template("register.html",message="表单信息不能为空")
        if len(username) > 20 or len(password) > 30 or len(useremail)> 30:
            return render_template("register.html",message="表单信息太长，请重新输入")
        if len(username) < 5 or len(password) < 5 or len(useremail) < 5:
            return render_template("register.html",message="表单信息太短，请重新输入")

