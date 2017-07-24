# coding: utf-8
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from nbd_news_scrapy_front import settings
import requests
import json
from datetime import datetime, timedelta
from django_celery_beat.models import PeriodicTask, IntervalSchedule, PeriodicTasks
from celery import shared_task
import logging


class XpathRuleSet(models.Model):
    # 对应着item对象
    # xpath_for_article_true_link = models.URLField(max_length=100)
    xpath_for_set_name = models.CharField(u'规则集名称', max_length=100, unique=True)
    xpath_for_no_article_true_link = models.CharField(u'单页抓取时通过该条件避免重复插入数据, 在没有article_ture_link时使用', max_length=50,
                                                      null=True,
                                                      blank=True)
    xpath_for_article_true_link = models.CharField(u'文章真实链接', max_length=100, blank=True, null=True)
    xpath_for_article_title = models.CharField(u'文章标题xpath', max_length=100)
    xpath_for_article_desc = models.CharField(u'文章描述xpath', max_length=100, blank=True)
    xpath_for_article_content = models.CharField(u'文章内容xpath', max_length=100, blank=True)
    xpath_for_article_origin = models.CharField(u'文章来源xpath', max_length=100, blank=True)
    xpath_for_article_published_at = models.CharField(u'文章发布时间xpath', max_length=100, blank=True)
    xpath_for_article_tags = models.CharField(u'文章标签或分类xpath', max_length=100, blank=True)

    class Meta:
        verbose_name = u'xpath规则配置'
        verbose_name_plural = u'xpath规则配置'

    def __unicode__(self):
        return self.xpath_for_set_name


class AllSiteCrawlConfig(models.Model):
    # crawl_type_choice = ((1, u'整站'), (2, u'特定链接'))
    # crawl_type = models.SmallIntegerField(u'爬虫类型', default=1, choices=crawl_type_choice)
    SCORE_CHOICES = [(0, u'一次更新'), ]
    SCORE_CHOICES = SCORE_CHOICES + zip(range(30, 121, 30), range(30, 121, 30))
    crawl_media = models.CharField(verbose_name=u'媒体域名(如:www.nbd.com.cn) 做关联用', max_length=30, unique=True)
    crawl_start_url = models.URLField(u'单个的start url(通常做快速更新的列表页)', unique=True)
    crawl_link_extractor_allow = models.CharField(u'LinkExtractor allow 正则', max_length=100, blank=True, null=True)
    crawl_link_extractor_deny = models.CharField(u'LinkExtractor deny 正则', max_length=100, blank=True, null=True)
    crawl_xpath_rule_set = models.ForeignKey(XpathRuleSet, verbose_name=u'item规则集')
    crawl_frequency = models.IntegerField(u'更新频率(单位：分钟)', choices=SCORE_CHOICES)
    crawl_note = models.CharField(u'start url备注', max_length=50, blank=True)
    crawl_scrapyd_jobid = models.CharField(u'scrapyd_jobid', max_length=35, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'AllSite数据源'
        verbose_name_plural = u'AllSite数据源管理'

    def __unicode__(self):
        return self.crawl_media


class CrawlDirSort(models.Model):
    push_type_choice = ((1, u'开启'), (0, u'关闭'))
    crawl_dir_sort_name = models.CharField(verbose_name=u'分类名称(通常为单个的start url的栏目名)', unique=True, max_length=30,
                                           db_index=True)
    crawl_push_status = models.SmallIntegerField(u'是否开启微信推送', choices=push_type_choice, default=0)

    class Meta:
        verbose_name = u'网站分类栏目'
        verbose_name_plural = u'网站分类栏目'

    def __unicode__(self):
        return self.crawl_dir_sort_name


class CrawlMedia(models.Model):
    crawl_domain = models.CharField(u"网站域名(根据域名生成allowed_domains)", max_length=200, default='', unique=True)
    crawl_media_name = models.CharField(verbose_name=u'网站名称(哪个网站,可在前端选网站，查看该网站的最新新闻)', unique=True, max_length=30,
                                        db_index=True)

    class Meta:
        verbose_name = u'网站'
        verbose_name_plural = u'网站'

    def __unicode__(self):
        return self.crawl_domain


class CrawlMediaSort(models.Model):
    crawl_media_sort_name = models.CharField(u'网站分类名称(通常为类别，如股票，财经)', unique=True, max_length=30, db_index=True)

    class Meta:
        verbose_name = u'网站分类'
        verbose_name_plural = u'网站分类'

    def __unicode__(self):
        return self.crawl_media_sort_name


class OnePageCrawlConfig(models.Model):
    status_type_choice = ((1, u'开启'), (2, u'关闭'))
    SCORE_CHOICES = [(0, u'一次更新'), ]
    SCORE_CHOICES = SCORE_CHOICES + zip(range(1, 10, 1), range(1, 10, 1))
    crawl_media = models.ForeignKey(CrawlMedia, verbose_name=u'网站域名(如:www.nbd.com.cn) 做关联用', db_index=True)
    crawl_media_sort = models.ForeignKey(CrawlMediaSort, verbose_name=u"网站分类(通常为类别，如股票，财经)", db_index=True)
    crawl_dir_sort = models.ForeignKey(CrawlDirSort, verbose_name=u'栏目分类(通常为单个的start url的栏目名)', db_index=True)
    crawl_start_url = models.URLField(u'单个的start url(通常做快速更新的列表页)', unique=True, db_index=True)
    crawl_xpath_rule_set = models.ForeignKey(XpathRuleSet, verbose_name=u'item规则集,该模型在当前页面获取')
    crawl_xpath_list = models.CharField(u'xpath规则，生成可循环的对象', max_length=100)
    crawl_frequency = models.IntegerField(u'更新频率(单位：分钟)', choices=SCORE_CHOICES)
    crawl_status = models.SmallIntegerField(u'是否开启抓取', choices=status_type_choice, default=1)
    crawl_note = models.CharField(u'start url备注', max_length=50, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'CurrentPage数据源'
        verbose_name_plural = u'CurrentPage数据源管理'

    def __unicode__(self):
        return self.crawl_media.crawl_domain


class JsonCrawlConfig(models.Model):
    status_type_choice = ((1, u'开启'), (2, u'关闭'))
    SCORE_CHOICES = [(0, u'一次更新'), ]
    SCORE_CHOICES = SCORE_CHOICES + zip(range(1, 10, 1), range(1, 10, 1))
    crawl_media = models.ForeignKey(CrawlMedia, verbose_name=u'网站域名(如:www.nbd.com.cn) 做关联用', db_index=True)
    crawl_media_sort = models.ForeignKey(CrawlMediaSort, verbose_name=u"网站分类(通常为类别，如股票，财经)", db_index=True)
    crawl_dir_sort = models.ForeignKey(CrawlDirSort, verbose_name=u'栏目分类(通常为单个的start url的栏目名)', db_index=True)
    crawl_start_url = models.URLField(u'单个的start url(通常做快速更新的列表页)', unique=True, db_index=True)
    crawl_xpath_rule_set = models.ForeignKey(XpathRuleSet, verbose_name=u'item规则集')
    crawl_next_url = models.CharField(u'提取当前json页面遍历数组(支持多级查找使用英文,隔开多个键)，不填写则在本页面上使用item规则集', max_length=100,
                                      blank=True, null=True)
    crawl_next_url_json_key = models.CharField(u'通过json键来提取数组中的中的url链接，不填写则在本页面上使用item规则集', max_length=20, blank=True,
                                               null=True)
    crawl_frequency = models.IntegerField(u'更新频率(单位：分钟)', choices=SCORE_CHOICES)
    crawl_status = models.SmallIntegerField(u'是否开启抓取', choices=status_type_choice, default=1)
    crawl_note = models.CharField(u'start url备注', max_length=50, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'Json数据源'
        verbose_name_plural = u'Json数据源管理'

    def __unicode__(self):
        return self.crawl_media.crawl_domain


class NextPageCrawlConfig(models.Model):
    status_type_choice = ((1, u'开启'), (2, u'关闭'))
    SCORE_CHOICES = [(0, u'一次更新'), ]
    SCORE_CHOICES = SCORE_CHOICES + zip(range(1, 30, 1), range(1, 30, 1))
    crawl_media = models.ForeignKey(CrawlMedia, verbose_name=u'网站域名(如:www.nbd.com.cn) 做关联用', db_index=True)
    crawl_media_sort = models.ForeignKey(CrawlMediaSort, verbose_name=u"网站分类(通常为类别，如股票，财经)", db_index=True)
    crawl_dir_sort = models.ForeignKey(CrawlDirSort, verbose_name=u'栏目分类(通常为单个的start url的栏目名)', db_index=True)
    crawl_start_url = models.URLField(u'单个的start url(通常做快速更新的列表页)', unique=True, db_index=True)
    crawl_link_extractor_allow = models.CharField(u'LinkExtractor allow 正则', max_length=100, blank=True, null=True)
    crawl_link_extractor_deny = models.CharField(u'LinkExtractor deny 正则', max_length=100, blank=True, null=True)
    crawl_xpath_rule_set = models.ForeignKey(XpathRuleSet, verbose_name=u'item规则集')
    crawl_frequency = models.IntegerField(u'更新频率(单位：分钟)', choices=SCORE_CHOICES)
    crawl_status = models.SmallIntegerField(u'是否开启抓取', choices=status_type_choice, default=1)
    crawl_note = models.CharField(u'start url备注', max_length=50, blank=True)
    crawl_scrapyd_jobid = models.CharField(u'scrapyd_jobid', max_length=35, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'NextPage数据源'
        verbose_name_plural = u'NextPage数据源管理'

    def __unicode__(self):
        return self.crawl_media.crawl_domain


class ReCrawlConfig(models.Model):
    status_type_choice = ((1, u'开启'), (2, u'关闭'))
    SCORE_CHOICES = [(0, u'一次更新'), ]
    SCORE_CHOICES = SCORE_CHOICES + zip(range(1, 10, 1), range(1, 10, 1))
    crawl_media = models.ForeignKey(CrawlMedia, verbose_name=u'网站域名(如:www.nbd.com.cn) 做关联用', db_index=True)
    crawl_media_sort = models.ForeignKey(CrawlMediaSort, verbose_name=u"网站分类(通常为类别，如股票，财经)", db_index=True)
    crawl_dir_sort = models.ForeignKey(CrawlDirSort, verbose_name=u'栏目分类(通常为单个的start url的栏目名)', db_index=True)
    crawl_start_url = models.URLField(u'单个的start url,获取next page链接', unique=True, db_index=True)
    crawl_xpath_rule_set = models.ForeignKey(XpathRuleSet, verbose_name=u'item规则集')
    crawl_next_url = models.CharField(u'提取当前json页面遍历数组(支持多级查找使用英文,隔开多个键)，不填写则在本页面上使用item规则集', max_length=100,
                                      blank=True, null=True)
    crawl_frequency = models.IntegerField(u'更新频率(单位：分钟)', choices=SCORE_CHOICES)
    crawl_status = models.SmallIntegerField(u'是否开启抓取', choices=status_type_choice, default=1)
    crawl_note = models.CharField(u'start url备注', max_length=50, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'正则提取数据源'
        verbose_name_plural = u'正则提取数据源管理'

    def __unicode__(self):
        return self.crawl_media.crawl_domain


@shared_task
def update_scrapy_crawl(**kwargs):
    data = {'project': kwargs['project'], 'spider': kwargs['spider'], 'crawl_start_url': kwargs['crawl_start_url']}
    # logging.log(logging.WARNING, data)
    r = requests.post(settings.SCRAPYD_SETTING_HOST + 'schedule.json', data=data).json()
    if r['status'] == "ok":
        return r['jobid']


@receiver(pre_save, sender=NextPageCrawlConfig)
def update_next_page_crawl(sender, instance, *args, **kwargs):
    print "fdsafads"
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=instance.crawl_frequency,
        period=IntervalSchedule.MINUTES,
    )
    logging.log(logging.DEBUG, schedule, created)
    if instance.id:
        print "log if instance"
        logging.log(logging.DEBUG, instance.id)
        old_customer_crawl_config = sender.objects.filter(pk=instance.id).first()
        print old_customer_crawl_config
        if instance.crawl_media != old_customer_crawl_config.crawl_media \
                or instance.crawl_start_url != old_customer_crawl_config.crawl_start_url \
                or instance.crawl_link_extractor_allow != old_customer_crawl_config.crawl_link_extractor_allow \
                or instance.crawl_link_extractor_deny != old_customer_crawl_config.crawl_link_extractor_deny \
                or instance.crawl_xpath_rule_set != old_customer_crawl_config.crawl_xpath_rule_set \
                or instance.crawl_frequency != old_customer_crawl_config.crawl_frequency \
                or instance.crawl_status != old_customer_crawl_config.crawl_status:
            # call scrapy crawl
            print instance.crawl_start_url
            logging.log(logging.DEBUG, instance.crawl_start_url)
            resp = requests.get(settings.SCRAPYD_SETTING_HOST + 'listprojects.json')
            project = resp.json()['projects'][0]
            data = {'project': project, 'spider': 'next_page_crawl', 'crawl_start_url': instance.crawl_start_url}
            task_status = True if instance.crawl_status == 1 else False
            expires_time = datetime.now() + timedelta(
                seconds=75) if instance.crawl_frequency == 0 else datetime.now() + timedelta(days=1000)
            PeriodicTask.objects.update_or_create(
                name=instance.crawl_start_url,
                defaults={'interval': schedule,
                          'task': 'scrapy_config.models.update_scrapy_crawl',
                          'name': instance.crawl_start_url,
                          'kwargs': json.dumps(data),
                          'enabled': task_status,
                          'expires': expires_time}
            )
    else:
        print 'no instance id'
        logging.log(logging.DEBUG, 'no instance id')
        resp = requests.get(settings.SCRAPYD_SETTING_HOST + 'listprojects.json')
        project = resp.json()['projects'][0]
        data = {'project': project, 'spider': 'next_page_crawl', 'crawl_start_url': instance.crawl_start_url}
        task_status = True if instance.crawl_status == 1 else False
        expires_time = datetime.now() + timedelta(
            seconds=75) if instance.crawl_frequency == 0 else datetime.now() + timedelta(days=1000)
        PeriodicTask.objects.update_or_create(
            name=instance.crawl_start_url,
            defaults={'interval': schedule,
                      'task': 'scrapy_config.models.update_scrapy_crawl',
                      'name': instance.crawl_start_url,
                      'enabled': task_status,
                      'kwargs': json.dumps(data),
                      'expires': expires_time}
        )


@receiver(pre_save, sender=OnePageCrawlConfig)
def update_one_page_crawl(sender, instance, *args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=instance.crawl_frequency,
        period=IntervalSchedule.MINUTES,
    )
    if instance.id:
        print "log if instance"
        logging.log(logging.DEBUG, instance.id)
        old_customer_crawl_config = sender.objects.filter(pk=instance.id).first()
        print old_customer_crawl_config
        if instance.crawl_media != old_customer_crawl_config.crawl_media \
                or instance.crawl_start_url != old_customer_crawl_config.crawl_start_url \
                or instance.crawl_xpath_list != old_customer_crawl_config.crawl_xpath_list \
                or instance.crawl_xpath_rule_set != old_customer_crawl_config.crawl_xpath_rule_set \
                or instance.crawl_frequency != old_customer_crawl_config.crawl_frequency \
                or instance.crawl_status != old_customer_crawl_config.crawl_status:
            # call scrapy crawl
            print instance.crawl_start_url
            logging.log(logging.DEBUG, instance.crawl_start_url)
            resp = requests.get(settings.SCRAPYD_SETTING_HOST + 'listprojects.json')
            project = resp.json()['projects'][0]
            data = {'project': project, 'spider': 'one_page_crawl', 'crawl_start_url': instance.crawl_start_url}
            task_status = True if instance.crawl_status == 1 else False
            expires_time = datetime.now() + timedelta(
                seconds=75) if instance.crawl_frequency == 0 else datetime.now() + timedelta(days=1000)
            PeriodicTask.objects.update_or_create(
                name=instance.crawl_start_url,
                defaults={'interval': schedule,
                          'task': 'scrapy_config.models.update_scrapy_crawl',
                          'name': instance.crawl_start_url,
                          'kwargs': json.dumps(data),
                          'enabled': task_status,
                          'expires': expires_time}
            )
    else:
        print 'no instance id'
        logging.log(logging.DEBUG, 'no instance id')
        resp = requests.get(settings.SCRAPYD_SETTING_HOST + 'listprojects.json')
        project = resp.json()['projects'][0]
        data = {'project': project, 'spider': 'one_page_crawl', 'crawl_start_url': instance.crawl_start_url}
        task_status = True if instance.crawl_status == 1 else False
        expires_time = datetime.now() + timedelta(
            seconds=75) if instance.crawl_frequency == 0 else datetime.now() + timedelta(days=1000)
        PeriodicTask.objects.update_or_create(
            name=instance.crawl_start_url,
            defaults={'interval': schedule,
                      'task': 'scrapy_config.models.update_scrapy_crawl',
                      'name': instance.crawl_start_url,
                      'enabled': task_status,
                      'kwargs': json.dumps(data),
                      'expires': expires_time}
        )


@receiver(pre_save, sender=JsonCrawlConfig)
def update_json_crawl(sender, instance, *args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=instance.crawl_frequency,
        period=IntervalSchedule.MINUTES,
    )
    if instance.id:
        print "log if instance"
        logging.log(logging.DEBUG, instance.id)
        old_customer_crawl_config = sender.objects.filter(pk=instance.id).first()
        print old_customer_crawl_config
        if instance.crawl_media != old_customer_crawl_config.crawl_media \
                or instance.crawl_start_url != old_customer_crawl_config.crawl_start_url \
                or instance.crawl_xpath_rule_set != old_customer_crawl_config.crawl_xpath_rule_set \
                or instance.crawl_next_url != old_customer_crawl_config.crawl_next_url \
                or instance.crawl_next_url_json_key != old_customer_crawl_config.crawl_next_url_json_key \
                or instance.crawl_frequency != old_customer_crawl_config.crawl_frequency \
                or instance.crawl_status != old_customer_crawl_config.crawl_status:
            # call scrapy crawl
            print instance.crawl_start_url
            logging.log(logging.DEBUG, instance.crawl_start_url)
            resp = requests.get(settings.SCRAPYD_SETTING_HOST + 'listprojects.json')
            project = resp.json()['projects'][0]
            data = {'project': project, 'spider': 'json_crawl', 'crawl_start_url': instance.crawl_start_url}
            task_status = True if instance.crawl_status == 1 else False
            expires_time = datetime.now() + timedelta(
                seconds=75) if instance.crawl_frequency == 0 else datetime.now() + timedelta(days=1000)
            PeriodicTask.objects.update_or_create(
                name=instance.crawl_start_url,
                defaults={'interval': schedule,
                          'task': 'scrapy_config.models.update_scrapy_crawl',
                          'name': instance.crawl_start_url,
                          'kwargs': json.dumps(data),
                          'enabled': task_status,
                          'expires': expires_time}
            )
    else:
        print 'no instance id'
        logging.log(logging.DEBUG, 'no instance id')
        resp = requests.get(settings.SCRAPYD_SETTING_HOST + 'listprojects.json')
        project = resp.json()['projects'][0]
        data = {'project': project, 'spider': 'json_crawl', 'crawl_start_url': instance.crawl_start_url}
        task_status = True if instance.crawl_status == 1 else False
        expires_time = datetime.now() + timedelta(
            seconds=75) if instance.crawl_frequency == 0 else datetime.now() + timedelta(days=1000)
        PeriodicTask.objects.update_or_create(
            name=instance.crawl_start_url,
            defaults={'interval': schedule,
                      'task': 'scrapy_config.models.update_scrapy_crawl',
                      'name': instance.crawl_start_url,
                      'enabled': task_status,
                      'kwargs': json.dumps(data),
                      'expires': expires_time}
        )