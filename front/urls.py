from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^guojun', views.guojun, name='guojun'),
    url(r'^receive_article_result', views.receive_article_result, name='receive_article_result'),
    url(r'^get_media_sorts', views.get_media_sorts, name='get_media_sorts'),
    url(r'^get_dir_sorts', views.get_dir_sorts, name='get_dir_sorts'),
    url(r'^get_medias', views.get_medias, name='get_medias'),
    url(r'^get_article', views.get_article, name='get_article'),
    # url(r'^login$', views.login, name='login'),
    # url(r'^logout$', views.logout, name='logout'),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
]

from django.conf import settings

if settings.DEBUG is False:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,
                                                                    }),
    ]
