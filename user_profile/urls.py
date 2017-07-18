from django.conf.urls import url
import views
from django.contrib.auth.views import login


urlpatterns = [
    url(r'^user/favorite', views.favorite, name='user_profile_favorite'),
    url(r'^user/logout', views.logout, name='user_profile_logout'),
    url(r'^user/login', login,{'template_name': 'user_profile/login.html'}, name='user_profile_login'),
]
