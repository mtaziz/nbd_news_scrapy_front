FROM scrapy_base
ADD . /data/
WORKDIR /data/
RUN pip install -r requirements.txt
# 不要使用& 后台执行
python manage.py runserver localhost:80