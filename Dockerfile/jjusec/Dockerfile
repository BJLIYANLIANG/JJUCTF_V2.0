FROM python
MAINTAINER hsm "905008677@qq.com"
WORKDIR /jjuctf_server
COPY ../../jjuctf ./jjuctf
COPY ../../app.py ./app.py
COPY ../../templates ./templates
COPY ../../static ./static
COPY ../../backup ./backup
COPY requirements.txt ./requirements.txt
#RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
#RUN  apt-get clean
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT python app.py