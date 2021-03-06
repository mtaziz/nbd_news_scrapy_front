# coding: utf-8
from django.contrib import admin
from models import AllSiteCrawlConfig, XpathRuleSet, NextPageCrawlConfig, CrawlDirSort, CrawlMedia, CrawlMediaSort, \
    OnePageCrawlConfig, JsonCrawlConfig, ReCrawlConfig
# from models import CrawlMedia
from django.contrib import messages
from django.utils.safestring import mark_safe


# Register your models here.
def batch_open(modeladmin, request, obj):
    obj.update(crawl_status=1)


def batch_close(modeladmin, request, obj):
    obj.update(crawl_status=0)


batch_close.short_description = u'批量关闭抓取'
batch_open.short_description = u'批量开启抓取'


class CrawlDirSortAdmin(admin.ModelAdmin):
    list_display = ('crawl_dir_sort_name', 'crawl_push_status_plus')
    list_per_page = 20
    search_fields = ('crawl_dir_sort_name',)
    actions = ['update_status_to_on', 'update_status_to_off']

    def update_status_to_on(self, request, obj=None):
        # need choose one at least
        obj.update(crawl_push_status=1)

    update_status_to_on.short_description = u'批量开启分类栏目推送'

    def update_status_to_off(self, request, obj=None):
        # need choose one at least
        obj.update(crawl_push_status=0)

    update_status_to_off.short_description = u'批量关闭分类栏目推送'

    def crawl_push_status_plus(self, obj):
        if obj.crawl_push_status == 1:
            return """<p class="btn btn-success">已开启</p>"""
        else:
            return """<p class="btn btn-danger">已关闭</p>"""

    crawl_push_status_plus.allow_tags = True
    crawl_push_status_plus.admin_order_field = 'crawl_push_status'
    crawl_push_status_plus.short_description = u"是否开启微信推送"


class CrawlMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'crawl_media_name')
    list_per_page = 20
    search_fields = ('crawl_domain','crawl_media_name')


class CrawlMediaSortAdmin(admin.ModelAdmin):
    list_display = ('id', 'crawl_media_sort_name')
    list_per_page = 20
    search_fields = ('crawl_media_sort_name',)


class AllSiteCrawlConfigAdmin(admin.ModelAdmin):
    list_display = (
        'crawl_media', 'crawl_start_url', 'crawl_link_extractor_allow', 'crawl_link_extractor_deny',
        'crawl_xpath_rule_set', 'crawl_note', 'crawl_frequency', 'crawl_scrapyd_jobid', 'updated_at')
    list_per_page = 50
    search_fields = ('crawl_start_url',)
    actions = [batch_open, batch_close]


class OnePageCrawlConfigAdmin(admin.ModelAdmin):
    list_display = (
        'crawl_start_url', 'crawl_media_sort', 'crawl_frequency', 'crawl_status_fri', 'updated_at')
    list_per_page = 50
    search_fields = ('crawl_start_url',)
    actions = [batch_open, batch_close]

    def crawl_status_fri(self, obj):
        if obj.crawl_status == 1:
            return """<p class="btn btn-success">已开启</p>"""
        else:
            return """<p class="btn btn-danger">已关闭</p>"""

    crawl_status_fri.allow_tags = True
    crawl_status_fri.admin_order_field = 'crawl_status'
    crawl_status_fri.short_description = u"是否开启抓取"


class JsonCrawlConfigAdmin(admin.ModelAdmin):
    list_display = (
        'crawl_start_url', 'crawl_media_sort', 'crawl_next_url', 'crawl_frequency', 'crawl_status_fri')
    list_per_page = 50
    search_fields = ('crawl_start_url',)
    actions = [batch_open, batch_close]

    def crawl_status_fri(self, obj):
        if obj.crawl_status == 1:
            return """<p class="btn btn-success">已开启</p>"""
        else:
            return """<p class="btn btn-danger">已关闭</p>"""

    crawl_status_fri.allow_tags = True
    crawl_status_fri.admin_order_field = 'crawl_status'
    crawl_status_fri.short_description = u"是否开启抓取"


class NextPageCrawlConfigAdmin(admin.ModelAdmin):
    list_display = (
        'crawl_start_url', 'crawl_media', 'crawl_media_sort', 'crawl_dir_sort', 'crawl_xpath_rule_set',
        'crawl_note', 'crawl_frequency', 'crawl_scrapyd_jobid', 'crawl_status_fri', 'updated_at')
    list_per_page = 50
    search_fields = ('crawl_start_url',)
    actions = [batch_open, batch_close]

    def crawl_status_fri(self, obj):
        if obj.crawl_status == 1:
            return """<p class="btn btn-success">已开启</p>"""
        else:
            return """<p class="btn btn-danger">已关闭</p>"""

    crawl_status_fri.allow_tags = True
    crawl_status_fri.admin_order_field = 'crawl_status'
    crawl_status_fri.short_description = u"是否开启抓取"


class ReCrawlConfigAdmin(admin.ModelAdmin):
    list_display = (
        'crawl_start_url', 'crawl_media_sort', 'crawl_next_url', 'crawl_frequency', 'crawl_status_fri')
    list_per_page = 50
    search_fields = ('crawl_start_url',)
    actions = [batch_open, batch_close]

    def crawl_status_fri(self, obj):
        if obj.crawl_status == 1:
            return """<p class="btn btn-success">已开启</p>"""
        else:
            return """<p class="btn btn-danger">已关闭</p>"""

    crawl_status_fri.allow_tags = True
    crawl_status_fri.admin_order_field = 'crawl_status'
    crawl_status_fri.short_description = u"是否开启抓取"


class XpathRuleSetAdmin(admin.ModelAdmin):
    list_display = ('xpath_for_set_name', 'xpath_for_article_title', 'xpath_for_article_true_link')
    list_per_page = 20
    search_fields = ('xpath_for_set_name', )


admin.site.register(AllSiteCrawlConfig, AllSiteCrawlConfigAdmin)
admin.site.register(NextPageCrawlConfig, NextPageCrawlConfigAdmin)
admin.site.register(XpathRuleSet, XpathRuleSetAdmin)
admin.site.register(CrawlMedia, CrawlMediaAdmin)
admin.site.register(CrawlMediaSort, CrawlMediaSortAdmin)
admin.site.register(CrawlDirSort, CrawlDirSortAdmin)
admin.site.register(OnePageCrawlConfig, OnePageCrawlConfigAdmin)
admin.site.register(JsonCrawlConfig, JsonCrawlConfigAdmin)
admin.site.register(ReCrawlConfig, ReCrawlConfigAdmin)
