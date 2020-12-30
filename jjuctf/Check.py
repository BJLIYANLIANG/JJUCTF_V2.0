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
    def checkflag(self,user,flag,challenge_id):
        # ctf_id就是CTF靶场id
        a = Mysqld()
        group_id = a.selectGroupInfoByUsername(user)
        # print(group_id)
        if group_id:
            groupid = group_id[0]
            # print(groupid)
            result  = a.checkFalg(groupid,flag,challenge_id)
        # result = 1
            if result:
                return 1
            else:
                return 0
        else:
            return 0


a = Check()
b = a.checkflag('test123',"flag{jjuctf}",1)
print(b)
# print(b)