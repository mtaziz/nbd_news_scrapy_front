FROM scrapy_base
ADD . /data/
WORKDIR /data/
RUN pip install -r requirements.txt
# 不要使用& 后台执行
ENTRYPOINT python manage.py runserver 0.0.0.0:80