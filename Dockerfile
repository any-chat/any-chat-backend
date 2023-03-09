FROM pypy:3.9-slim-buster as build-stage

# 不生成pyc文件
ENV PYTHONDONTWRITEBYTECODE=1
# 打印日志不使用缓存
ENV PYTHONUNBUFFERED=1

RUN sed -i s/deb.debian.org/mirrors.aliyun.com/g /etc/apt/sources.list
RUN apt-get update && apt-get install -y libjpeg-dev zlib1g-dev

RUN mkdir -p /app
WORKDIR /app

COPY ./requirements.txt ./

# 换源
RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple
RUN pip config set install.trusted-host mirrors.cloud.com

# 升级pip
RUN pip install --upgrade pip

# 安装依赖
RUN pip install -r requirements.txt

# 复制代码
COPY . .


EXPOSE 8088
ENTRYPOINT ["gunicorn", "-c", "gunicorn.conf", "anychat.asgi:application"]