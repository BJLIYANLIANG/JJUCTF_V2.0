import yagmail
from jjuctf.config import *
class MailServer:
    def sendMail(self,email_to,email_title,email_content):
        mail_server = yagmail.SMTP(user=mail_user,password=mail_key,host=mail_host)
        # email_attachements = ['xxx/xxx.jpg']
        mail_server.send(email_to,email_title,email_content,attachments=None)
        mail_server.close()

email_to = '2621861508@qq.com'
email_title = 'JJUCTF注册'
email_content = 'hello world'
a = MailServer()
a.sendMail(email_to,email_title,email_content)