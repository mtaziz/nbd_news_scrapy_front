# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_favorite_crawl_media_sort = models.CharField(max_length=1000, default='')
    user_favorite_crawl_media = models.CharField(max_length=1000, default='')
    user_favorite_crawl_dir_sort = models.CharField(max_length=1000, default='')

    def __unicode__(self):
        return self.user.first_name

    class Meta:
        verbose_name = u'用户详情'
        verbose_name_plural = u"用户详情"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)