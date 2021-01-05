import time
a = "2021-01-05 11:05:43"
def checkCompetition_start(start_time,end_time):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    year, moon, day, h, m, s = splitdatetime(date)
    start_year, start_moon, start_day, start_h, start_m, start_s = splitdatetime(start_time)
    end_year, end_moon, end_day, end_h, end_m, end_s = splitdatetime(date)
    if year>=start_year and year<=end_year:
        if moon>=start_moon and moon<=end_moon:
            if day>=start_day and day <= end_day:
                if h >= start_h and h<=end_h:
                    if m >= start_m and h<=end_m:
                        if s>=start_s and s<=end_s:
                            return 1
                        return 0
                    return 0
                return 0
            return 0
        return 0
    return 0
def splitdatetime(datetime):
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
result = checkCompetition_start("2021-01-03 11:05:43","2021-01-04 10:05:43")
print(result)

