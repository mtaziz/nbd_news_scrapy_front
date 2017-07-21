from django.conf.urls import url
import views
from django.contrib.auth.views import login


urlpatterns = [
    url(r'^user/favorite', views.favorite, name='user_profile_favorite'),
    url(r'^user/update_favorite', views.update_favorite, name='user_profile_update_favorite'),
    url(r'^user/logout', views.logout, name='user_profile_logout'),
    url(r'^user/help', views.help, name='user_profile_help'),
    url(r'^user/setting', views.setting, name='user_profile_setting'),
    url(r'^user/login', login,{'template_name': 'user_profile/login.html'}, name='user_profile_login'),
]
