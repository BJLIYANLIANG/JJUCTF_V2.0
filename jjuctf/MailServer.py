import yagmail
from jjuctf.config import *
# key = 'YAXRVNWCUVZIBNPD'
class MailServer:
    def sendMail(self,email_to,email_title,email_content):
        mail_server = yagmail.SMTP(user=mail_user,password=mail_key,host=mail_host)
        # email_attachements = ['xxx/xxx.jpg']
        mail_server.send(email_to,email_title,email_content,attachments=None)
        mail_server.close()


#
# email_to = '905008677@qq.com'
# email_title = 'JJUCTF注册'
# email_content = '欢迎注册九江学院网络安全靶场实训平台，注册码：897799'
# a = MailServer()
# a.sendMail(email_to)