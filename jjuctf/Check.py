import re
import time


def check_input(login_string):
    login_string = str(login_string).lower()
    pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
    r = re.search(pattern, login_string)
    if r:
        print('检测到有sql注入！')
        return 0
    else:
        print(login_string.find('\''))
        if login_string.find('\'') != -1 or login_string.find('\"') != -1 or login_string.find('\#') != -1:
            return 0
        return 1
# 只能有大小写字符和数字

def check_Username_And_Passwd_And_Email(username, password, useremail):
    if username == '' or password == '' or useremail == '':
        print("输入的字符串为空！")
        return 0
    if len(username) > 6 or len(password) > 6 or len(useremail) > 6:
        if len(username) < 100 or len(password) < 100 or len(useremail) < 100:
            if check_input(username):
                if check_input(password):
                    if check_input(useremail):
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



def check_sql_insert(str):
    # 检查sql注入
    if str == '':
        return 0
    else:
        return 1


def check_is_valid_email(email):
    ex_email = re.compile(r'^[1-9][0-9]{4,10}@.*\..*')
    result = ex_email.match(email)
    # print(result)
    if result:
        # 邮箱合法
        return 1
    else:
        # 不合法
        return -1

class Check:
    def __init__(self):
        pass

    # 检测sql注入


    # 检查是否是比赛时间，如果是则返回1,不是则返回0
    def checkCompetition_start(self, start_time, end_time):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if current_time.__ge__(start_time) and current_time.__le__(end_time):
            return 1
        else:
            if current_time.__lt__(start_time):
                return 0
            else:
                return 2

