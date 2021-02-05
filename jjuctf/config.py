# redis config
redis_address = 'localhost'
redis_port = '6379'
# user='',,host='smtp.163.com'
# Mail Config
mail_user = 'hsmcool@163.com'
# 授权码
mail_key = 'YAXRVNWCUVZIBNPD'
# smtp服务器
mail_host = 'smtp.163.com'
class Config:
    def __init__(self):
        self.serverIp = "localhost"
        self.user = "root"
        self.database = 'jjuctf'
        self.password = "905008"  # 数据库密码，宝塔面板
        self.tokenKey = "test@124"
        self.redis_address = 'localhost'
        self.redis_port = '6379'