import re
import time


def checksqlSecure(sql):
    sql = str(sql).lower()
    pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char" \
              r"|delclare|or)\b|(\*|;) "
    r = re.search(pattern, sql)
    # print(r)
    if r:
        print('检测到有sql注入！')
        return 0
    else:
        return 1


def check_Username_And_Passwd_And_Email(username, password, useremail):
    if username == '' or password == '' or useremail == '':
        print("输入的字符串为空！")
        return 0
    if len(username) > 6 or len(password) > 6 or len(useremail) > 6:
        if len(username) < 100 or len(password) < 100 or len(useremail) < 100:
            if checksqlSecure(username):
                if checksqlSecure(password):
                    if checksqlSecure(useremail):
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

