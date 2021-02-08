from threading import Timer
import datetime
# 每隔两秒执行一次任务
def printHello():
    print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    t = Timer(60, printHello)
    t.start()

if __name__ == "__main__":
    printHello()