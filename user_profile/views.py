from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json


# Create your views here.
@login_required
def favorite(request):
    current_user_profile = User.objects.get(id=request.user)
    user_favorite_info = {}
    user_favorite_info['user_favorite_crawl_media_sort'] = current_user_profile
    # user_favorite_info['user_favorite_crawl_media'] = current_user_profile.user_favorite_crawl_media
    # user_favorite_info['user_favorite_crawl_dir_sort'] = current_user_profile.user_favorite_crawl_media
    return HttpResponse(json.dumps(user_favorite_info), content_type="application/json")
