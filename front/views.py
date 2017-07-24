# coding: utf8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from scrapy_config.models import CrawlMedia, CrawlMediaSort, CrawlDirSort
import json
from django.core.urlresolvers import reverse
import logging
from django.contrib.auth.decorators import login_required
from django.core import serializers
from scrapy_config.models import NextPageCrawlConfig
from itertools import chain
from django.db.models import Q
import time
from front.models import Articles, ArticleForm
from haystack.generic_views import SearchView


def check_user_is_login(func):
    def wrapper(request, *args, **kwargs):
        cookies = request.COOKIES
        if cookies.get('user_name') and cookies.get('customer_id'):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login')

    return wrapper


# Create your views here.
@login_required(login_url="/user/login/")
def index(request):
    return render(request, 'front/index.html', locals())


@login_required(login_url="/user/login/")
def home(request):
    return render(request, 'front/home.html')


@login_required(login_url="/user/login/")
def get_article_detail(request, detail_id):
    detail_info = get_object_or_404(Articles, id=detail_id)
    return render(request, 'front/detail.html', locals())


def receive_article_result(request):
    if request.method == 'POST':
        article_info = ArticleForm(request.POST)
        updated_values = {}
        for key, value in request.POST.items():
            updated_values[key] = value

        updated_values['article_for_crawl_media'] = CrawlMedia.objects.get(id=updated_values['article_for_crawl_media'])
        updated_values['article_for_crawl_media_sort'] = CrawlMediaSort.objects.get(
            id=updated_values['article_for_crawl_media_sort'])
        updated_values['article_for_crawl_dir_sort'] = CrawlDirSort.objects.get(
            id=updated_values['article_for_crawl_dir_sort'])
        if article_info.is_valid():
            article_info = Articles.objects.create(**updated_values)
            article_info.save()
            return HttpResponse(json.dumps({'status': 200, 'message': 'success'}), content_type="application/json")
        else:
            print article_info.errors
            return HttpResponse(json.dumps({'status': 500, 'message': 'failed'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': 500, 'message': 'failed'}), content_type="application/json")


@login_required(login_url="/user/login/")
def get_article(request):
    current_time = request.GET.get("SendTime", '')
    # newCurArticleClassify 文章标签
    # newCurPlatform 文章平台
    all_articles_info_list = []
    newCurArticleClassifyl = request.GET.get("user_favorite_crawl_media_sort", '').split(",")
    article_info_list_for_media_sort = []
    if newCurArticleClassifyl != [u'']:
        media_sort_list = []
        for i in newCurArticleClassifyl:
            media_sort_list.append(int(i.split("_")[0]))
        article_info_list_for_media_sort = Articles.objects.filter(
            article_for_crawl_media_sort__in=media_sort_list).order_by('-article_updated_at')[:20]

    Platforml = request.GET.get("user_favorite_crawl_dir_sort", '').split(",")
    article_info_list_for_dir_sort = []
    if Platforml != [u'']:
        dir_sort_list = []
        for i in Platforml:
            dir_sort_list.append(int(i.split("_")[0]))
        article_info_list_for_dir_sort = Articles.objects.filter(
            article_for_crawl_dir_sort__in=dir_sort_list).order_by(
            '-article_updated_at')[:10]

    Allmedia = request.GET.get("user_favorite_crawl_media", '').split(",")
    article_info_list_for_media = []
    if Allmedia != [u'']:
        media_list = []
        for i in Allmedia:
            media_list.append(int(i.split("_")[0]))
        # if current_time:
        #     last_updated_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(current_time) / 1000))
        #     article_info_list_for_media = Articles.objects.filter(article_for_crawl_media_sort__in=media_list,
        #                                                           article_updated_at__gte=last_updated_time).order_by(
        #         'article_updated_at')[:20]
        # else:
        article_info_list_for_media = Articles.objects.filter(article_for_crawl_media__in=media_list).order_by(
            '-article_updated_at')[:20]

    for j in chain(article_info_list_for_media_sort, article_info_list_for_dir_sort, article_info_list_for_media):
        single_info = {}
        single_info['pk'] = j.id
        single_info['link'] = reverse('get_article_detail', kwargs={"detail_id": j.id})
        single_info['media_name'] = j.article_for_crawl_media.crawl_media_name
        single_info['article_published_at'] = str(j.article_published_at)
        single_info['article_true_link'] = j.article_true_link
        single_info['article_title'] = j.article_title
        single_info['article_desc'] = j.article_desc
        single_info['article_content'] = j.article_content
        single_info['article_tags'] = j.article_tags
        all_articles_info_list.append(single_info)
    return HttpResponse(json.dumps(all_articles_info_list), content_type="application/json")


@login_required(login_url="/user/login/")
def get_medias(request):
    media_info = CrawlMedia.objects.all().values('id', 'crawl_media_name')
    media_list = []
    for i in media_info:
        media_list.append({
            'crawl_media_name': i['crawl_media_name'],
            'id': str(i['id']) + "_get_medias"
        })
    return HttpResponse(json.dumps({'status': 200, 'message': media_list}), content_type="application/json")


@login_required(login_url="/user/login/")
def get_media_sorts(request):
    media_sort_info = CrawlMediaSort.objects.all().values('id', 'crawl_media_sort_name')
    media_list = []
    for i in media_sort_info:
        media_list.append({
            'crawl_media_sort_name': i['crawl_media_sort_name'],
            'id': str(i['id']) + "_get_media_sorts"
        })
    return HttpResponse(json.dumps({'status': 200, 'message': media_list}), content_type="application/json")


@login_required(login_url="/user/login/")
def get_dir_sorts(request):
    media_sort_info = CrawlDirSort.objects.all().values('id', 'crawl_dir_sort_name')
    media_list = []
    for i in media_sort_info:
        media_list.append({
            'crawl_dir_sort_name': i['crawl_dir_sort_name'],
            'id': str(i['id']) + "_get_dir_sorts"
        })
    return HttpResponse(json.dumps({'status': 200, 'message': media_list}), content_type="application/json")


def login(request):
    return render(request, 'front/logain.html', locals())


def get_favicon(request):
    return HttpResponse('')


class KeyWordSearchView(SearchView):
    template_name = "front/search.html"

    # load_all = False
    def get_queryset(self):
        queryset = super(KeyWordSearchView, self).get_queryset()
        query_word = self.request.GET.get('q', '')
        return queryset.filter(content=query_word).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(KeyWordSearchView, self).get_context_data(**kwargs)
        context['customer_id'] = "pass"
        context['user_name'] = "pass"
        return context

    def paginate_queryset(self, queryset, page_size):
        return super(KeyWordSearchView, self).paginate_queryset(queryset[:200], page_size)
