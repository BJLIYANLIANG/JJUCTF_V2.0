workers = 2   #定义同时开启的处理请求的进程数量，根据网站流量适当调整
worker_class = "eventlet"
bind = "0.0.0.0:8000"
