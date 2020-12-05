FROM python:3.8
WORKDIR /Project/demo

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
CMD ["gunicorn","start:app","-c","./gunicorn.conf.py"]

