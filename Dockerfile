FROM scrapy_base
ADD ./requirements.txt /data/requirements.txt
RUN pip install -r /data/requirements.txt
ADD . /data/
WORKDIR /data/
RUN python manage.py collectstatic  --noinput
# 不要使用& 后台执行
ENTRYPOINT python manage.py runserver 0.0.0.0:80