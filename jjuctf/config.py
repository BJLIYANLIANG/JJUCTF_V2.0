# redis config
redis_address = 'localhost'
redis_port = '6379'

class Config:
    def __init__(self):
        self.serverIp = "localhost"
        self.user = "root"
        self.database = 'jjuctf'
        self.password = "905008"  # 数据库密码，宝塔面板
        self.tokenKey = "test@124"
        self.redis_address = 'localhost'
        self.redis_port = '6379'