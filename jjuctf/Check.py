from jjuctf.man_Sql import Mysqld
import re
class Check:
    def __init__(self):
        pass
    def check_Username_And_Passwd_And_Email(self,username,password,useremail):
        if username == '' or password == '' or useremail == '':
            print("输入的字符串为空！")
            return 0
        if len(username) > 6 or len(password) > 6 or len(useremail)> 6:
            if len(username) < 100 or len(password) < 100 or len(useremail) < 100:
                if self.checksqlSecure(username):
                    if self.checksqlSecure(password):
                        if self.checksqlSecure(useremail):
                            return 1
                        return 0
                    return 0
                return 0
            else:
                print("字符串长度过长！")
                return 0
        else:
            print("字符串长度过短！")
            return 0


    def checksqlSecure(self,sql):
        sql = str(sql).lower()
        pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
        r = re.search(pattern, sql)
        print(r)
        if r:
            print('检测到有sql注入！')
            return 0
        else:
            return 1
    # 检查flag是否正确

#
# a = Check()
# b = a.checksqlSecure("select;ssadsdfdsa")
# print(b)
# b = a.checkflag('test123',"flag{jjuctf}",1)
# print(b)
# print(b)