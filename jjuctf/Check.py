import re
import time
import datetime
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

    #检测sql注入
    def checksqlSecure(self,sql):
        sql = str(sql).lower()
        pattern = r"\b(and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or)\b|(\*|;)"
        r = re.search(pattern, sql)
        # print(r)
        if r:
            print('检测到有sql注入！')
            return 0
        else:
            return 1

    # 检查是否是比赛时间，如果是则返回1,不是则返回0
    def checkCompetition_start(self,start_time, end_time):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # type(current_time)
        if current_time.__ge__(start_time) and current_time.__le__(end_time):
            return 1
        else:
            if current_time.__lt__(start_time):
                return 0
            else:
                return 2
        # print(date)
        # year, moon, day, h, m, s = self.splitdatetime(date)
        # print(year, moon, day, h, m, s)
        # start_year, start_moon, start_day, start_h, start_m, start_s = self.splitdatetime(start_time)
        # print(start_year, start_moon, start_day, start_h, start_m, start_s)
        # end_year, end_moon, end_day, end_h, end_m, end_s = self.splitdatetime(end_time)
        # print(end_year, end_moon, end_day, end_h, end_m, end_s)




                    # 2020-7-7 14:14 start
                    # 2021-1-1 1:11 current
                    # 2021-7-7 14:14 end


    def splitdatetime(self,datetime):
        a = datetime.split('-')
        b = a[2].split(' ')
        c = b[1].split(':')
        year = a[0]
        moon = a[1]
        day = b[0]
        h = c[0]
        m = c[1]
        s = c[2]
        return (year, moon, day, h, m, s)


# current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# a = Check(
# b = a.checksqlSecure()
# print(b)
# b = a.checkflag('test123',"flag{jjuctf}",1)
# print(b)
# print(b)