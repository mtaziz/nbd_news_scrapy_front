FROM scrapy_base
ADD ./requirements.txt /data/requirements.txt
RUN pip install -r /data/requirements.txt
ADD . /data/
WORKDIR /data/
RUN python manage.py collectstatic  --noinput -v 0 
# 不要使用& 后台执行 ，后台执行后会导致k8s认为pod dead

ENTRYPOINT python manage.py runserver 0.0.0.0:80