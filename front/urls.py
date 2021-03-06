from django.conf.urls import url
import views
from views import KeyWordSearchView
from django.views.static import serve as staticserve
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^search/', login_required(KeyWordSearchView.as_view(), login_url="/admin/login/"), name='haystack_search'),

    url(r'^$', views.home, name='home'),
    # url(r'^index.html$', views.index, name='index'),
    url(r'^receive_article_result', views.receive_article_result, name='receive_article_result'),
    url(r'^get_media_sorts', views.get_media_sorts, name='get_media_sorts'),
    url(r'^get_dir_sorts', views.get_dir_sorts, name='get_dir_sorts'),
    url(r'^get_medias', views.get_medias, name='get_medias'),
    url(r'^get_article', views.get_article, name='get_article'),
    url(r'^detail/(?P<detail_id>\d+?)\.html', views.get_article_detail, name='get_article_detail'),
    url(r'^update_article_tags/(?P<detail_id>\d+)', views.update_article_tags, name='update_article_tags'),
    url(r'^create_article_tags/(?P<detail_id>\d+)', views.create_article_tags, name='create_article_tags'),
    url(r'^create_article_desc/(?P<detail_id>\d+)', views.create_article_desc, name='create_article_desc'),
    url(r'^favicon.ico$', views.get_favicon, name='get_favicon'),
    # url(r'^logout$', views.logout, name='logout'),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
]

from django.conf import settings

if settings.DEBUG is False:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', staticserve, {'document_root': settings.MEDIA_ROOT, }),
         url(r'^static/(?P<path>.*)$', staticserve, {'document_root': settings.STATIC_ROOT}),
    ]
