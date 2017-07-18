from django.conf.urls import url
import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^user/favorite$', views.favorite, name='favorite'),
]
