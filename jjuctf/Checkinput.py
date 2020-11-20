from flask import render_template
class Checkinnput:
    def __init__(self):
        pass
    def checkUserString(self,username,password,useremail):
        if username == '' or password == '' or useremail == '':
            return 0
        if len(username) > 20 or len(password) > 30 or len(useremail)> 30:
            return 0
        if len(username) < 5 or len(password) < 5 or len(useremail) < 5:
            return 0
        return 1

