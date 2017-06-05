# coding: utf8
from django.contrib import admin
from models import Articles, ArticleTag, ArticlePushConfig, WechatQiyeConfig, WechatDepartment


# Register your models here.


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('article_true_link', 'article_for_crawl_media', 'article_link_for_md5code', 'article_updated_at')
    list_per_page = 50
    actions = ['delete_all_data']

    def delete_all_data(self, request, obj=None):
        # need choose one at least
        Articles.objects.all().delete()

    delete_all_data.short_description = u'删除所有数据'


class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'updated_at')
    list_per_page = 50
    actions = ['delete_all_data']

    def delete_all_data(self, request, obj=None):
        # need choose one at least
        ArticleTag.objects.all().delete()

    delete_all_data.short_description = u'删除所有数据'


class WechatQiyeConfigAdmin(admin.ModelAdmin):
    list_display = (
        'wechat_qiye_name', 'wechat_corp_id', 'wechat_corp_access_token', 'wechat_corp_access_token_expires_time')

    def has_add_permission(self, request):
        count = WechatQiyeConfig.objects.all().count()
        if count == 0:
            return True
        return False


class ArticlePushConfigAdmin(admin.ModelAdmin):
    list_display = ('wechat_user', 'push_status_plus', 'updated_at', 'wechat_user_for_department_display')
    actions = ['update_status_to_on', 'update_status_to_off']

    def wechat_user_for_department_display(self, obj):
        return ','.join([i.department_name for i in obj.wechat_user_for_department.all()])
    wechat_user_for_department_display.short_description = u"用户所属部门组"

    def update_status_to_off(self, request, obj=None):
        # need choose one at least
        obj.update(push_status=0)

    def update_status_to_on(self, request, obj=None):
        # need choose one at least
        obj.update(push_status=1)

    update_status_to_on.short_description = u'批量开启账号推送'
    update_status_to_off.short_description = u'批量关闭账号推送'

    def push_status_plus(self, obj):
        if obj.push_status == 1:
            return """<p class="btn btn-success">已开启</p>"""
        else:
            return """<p class="btn btn-danger">已关闭</p>"""

    push_status_plus.allow_tags = True
    push_status_plus.admin_order_field = 'crawl_push_status'
    push_status_plus.short_description = u"是否开启微信推送"


class WechatDepartmentAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('department_id', 'department_name', 'id')




admin.site.register(Articles, ArticlesAdmin)
admin.site.register(ArticleTag, ArticleTagAdmin)
admin.site.register(ArticlePushConfig, ArticlePushConfigAdmin)
admin.site.register(WechatQiyeConfig, WechatQiyeConfigAdmin)
admin.site.register(WechatDepartment, WechatDepartmentAdmin)
