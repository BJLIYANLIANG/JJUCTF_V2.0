from flask import render_template
from jjuctf.man_Sql import Mysqld
class Check:
    def __init__(self):
        pass
    def checkUserString(self,username,password,useremail,password2):
        if username == '' or password == '' or useremail == '':
            return 0
        if len(username) > 20 or len(password) > 30 or len(useremail)> 30:
            return 0
        if len(username) < 5 or len(password) < 5 or len(useremail) < 5:
            return 0
        return 1



    # 检查flag是否正确
    def checkflag(self,user,challenge_id,flag):
        # ctf_id就是CTF靶场id
        a = Mysqld()
        group_id = a.selectGroupByusername(user)
        group_id = 2
        result  = a.checkFalg(group_id,flag,challenge_id)
        if result:
            return 1
        else:
            return 0

