# coding=utf-8
from django.db import models
from django.forms import ModelForm
from scrapy_config.models import CrawlMedia, CrawlMediaSort, CrawlDirSort
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
import requests
from datetime import datetime, timedelta
import json
from nbd_news_scrapy_front import settings
import logging


# Create your models here.
class ArticleTag(models.Model):
    tag_name = models.CharField(u'分类标签', max_length=20, default="新闻")
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.tag_name

    class Meta:
        verbose_name = u"标签名称"
        verbose_name_plural = u"标签名称"


class Articles(models.Model):
    article_true_link = models.CharField(u'来源链接', max_length=150)
    article_link_for_md5code = models.CharField(u'链接MD5码', max_length=32, db_index=True, unique=True)
    article_for_crawl_media = models.ForeignKey(CrawlMedia, verbose_name=u'网站域名(如:www.nbd.com.cn) 做关联用', max_length=30)
    article_for_crawl_media_sort = models.ForeignKey(CrawlMediaSort, verbose_name=u"网站分类(通常为类别，如股票，财经)", db_index=True)
    article_for_crawl_dir_sort = models.ForeignKey(CrawlDirSort, verbose_name=u'栏目分类(通常为单个的start url的栏目名)',
                                                   db_index=True)
    article_title = models.CharField(u'来源标题', max_length=150)
    article_desc = models.TextField(u'来源摘要', blank=True, default='')
    article_content = models.TextField(u'来源内容', blank=True, default='')
    article_origin = models.CharField(u'上级来源', max_length=20, default='', blank=True, null=True)
    article_published_at = models.DateTimeField(u'来源发布时间')
    article_tags = models.CharField(u'相关标签', max_length=20, default='')
    article_updated_at = models.DateTimeField(u'抓取时间', auto_now=True)

    def __unicode__(self):
        return self.article_true_link

    class Meta:
        verbose_name_plural = u"文章信息"
        verbose_name = u"文章信息"


class ArticleForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['article_true_link', 'article_link_for_md5code', 'article_title', 'article_desc',
                  'article_content', 'article_origin', 'article_published_at', 'article_tags']


class WechatDepartment(models.Model):
    department_id = models.SmallIntegerField(u"成员所属部门id", default=3, unique=True)
    department_name = models.CharField(u"部门名称", default=u"实时新闻", unique=True, max_length=100)
    class Meta:
        verbose_name_plural = u"微信企业号部门"
        verbose_name = u"微信企业号部门"

    def __unicode__(self):
        return self.department_name


class ArticlePushConfig(models.Model):
    push_status_type = ((1, '开启'), (0, '关闭'))
    wechat_user = models.CharField(u"需要推送的微信账号，需要关注企业号", max_length=20, default='')
    wechat_user_for_department = models.ManyToManyField(WechatDepartment,verbose_name=u"微信企业号部门名称")
    push_status = models.SmallIntegerField(u'当前状态', choices=push_status_type, default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = u"微信账号推送管理"
        verbose_name = u"微信账号"

    def __unicode__(self):
        return self.wechat_user


class WechatQiyeConfig(models.Model):
    wechat_qiye_name = models.CharField(u"微信企业号名称，备注使用", max_length=20, default='')
    wechat_corp_id = models.CharField(u"微信corp_id", max_length=20, default='')
    wechat_corp_secret = models.CharField(u"微信corp_secret", max_length=66, default='')
    wechat_corp_access_token = models.TextField(u"access_token", max_length=66, default='', blank=True, null=True)
    wechat_corp_access_token_expires_time = models.DateTimeField(u"access_token过期时间", auto_now=True)
    wechat_corp_access_token_updated_at = models.DateTimeField(u"access_token更新时间", auto_now=True)

    class Meta:
        verbose_name_plural = u"微信企业号设置"
        verbose_name = u"微信企业号"

    def __unicode__(self):
        return self.wechat_qiye_name


@receiver(post_save, sender=WechatQiyeConfig)
def update_access_token(sender, instance, *args, **kwargs):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + instance.wechat_corp_id + '&corpsecret=' + instance.wechat_corp_secret
    logging.log(logging.DEBUG, gettoken_url)
    resp = requests.get(gettoken_url)
    if resp.status_code == 200:
        instance.wechat_corp_access_token = resp.json()['access_token']
        instance.wechat_corp_access_token_expires_time = datetime.now() + timedelta(seconds=resp.json()['expires_in'])
        sender.objects.filter(pk=instance.id).update(wechat_corp_access_token=instance.wechat_corp_access_token,
                                                     wechat_corp_access_token_expires_time=instance.wechat_corp_access_token_expires_time)


@receiver(post_save, sender=Articles)
def push_article_to_wechat(sender, instance, *args, **kwargs):
    # if action == "post_add":
    if instance.article_for_crawl_dir_sort.crawl_push_status == 1:
        wechat_info = WechatQiyeConfig.objects.first()
        if wechat_info and (wechat_info.wechat_corp_access_token_expires_time > datetime.now()):
            send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + wechat_info.wechat_corp_access_token
            user_list = []
            for user in ArticlePushConfig.objects.filter(push_status=1).values('wechat_user'):
                user_list.append(user['wechat_user'])
            logging.log(logging.DEBUG, user_list)
            send_values = {
                "touser": "|".join(user_list),
                "msgtype": "text",
                "agentid": "0",
                "text": {
                    "content": instance.article_content + "\n" + instance.article_for_crawl_media.crawl_media_name
                },
                "safe": "0"
            }
            data = json.dumps(send_values, ensure_ascii=False).encode('utf8')
            resp = requests.post(send_url, data=data)
            print resp.content
        elif wechat_info and (wechat_info.wechat_corp_access_token_expires_time < datetime.now()):
            wechat_info.save()
            send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + wechat_info.wechat_corp_access_token
            user_list = []
            for user in ArticlePushConfig.objects.filter(push_status=1).values('wechat_user'):
                user_list.append(user['wechat_user'])
            send_values = {
                "touser": "|".join(user_list),
                "msgtype": "text",
                "agentid": "0",
                "text": {
                    "content": instance.article_content + "\n" + instance.article_for_crawl_media.crawl_media_name
                },
                "safe": "0"
            }
            data = json.dumps(send_values, ensure_ascii=False).encode('utf8')
            resp = requests.post(send_url, data=data)
            print resp.content


@receiver(post_save, sender=ArticlePushConfig)
def add_wechat_user_to_qiye(sender, instance, *args, **kwargs):
    wechat_user_for_department_list = instance.wechat_user_for_department.all()
    # if wechat_user_for_department_list:
    #     print "youle"
    # else:
    #     print "no"
    if wechat_user_for_department_list:
        department_id_list = [i.department_id for i in  instance.wechat_user_for_department.all()]
        wechat_info = WechatQiyeConfig.objects.first()
        send_url = settings.WECHAT_CREATE_USER_API + wechat_info.wechat_corp_access_token
        send_values = {
            "userid": instance.wechat_user,
            "name": instance.wechat_user,
            "department": department_id_list,
            "weixinid": instance.wechat_user,
        }
        logging.log(logging.WARN, send_values)
        data = json.dumps(send_values, ensure_ascii=False).encode('utf8')
        resp = requests.post(send_url, data=data)
        if resp.json()['errmsg']== "userid existed":
            send_url = settings.WECHAT_UPDATE_USER_API + wechat_info.wechat_corp_access_token
            resp = requests.post(send_url, data=data)
            print resp.content


