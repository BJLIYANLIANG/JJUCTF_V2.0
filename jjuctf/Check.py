import re
import time
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
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(date)
        year, moon, day, h, m, s = self.splitdatetime(date)
        start_year, start_moon, start_day, start_h, start_m, start_s = self.splitdatetime(start_time)
        end_year, end_moon, end_day, end_h, end_m, end_s = self.splitdatetime(date)
        if year >= start_year and year <= end_year:
            if moon >= start_moon and moon <= end_moon:
                if day >= start_day and day <= end_day:
                    if h >= start_h and h <= end_h:
                        if m >= start_m and h <= end_m:
                            if s >= start_s and s <= end_s:
                                return 1
                            return 0
                        return 0
                    return 0
                return 0
            return 0
        return 0

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
# a = Check()
# b = a.checksqlSecure("select;ssadsdfdsa")
# print(b)
# b = a.checkflag('test123',"flag{jjuctf}",1)
# print(b)
# print(b)