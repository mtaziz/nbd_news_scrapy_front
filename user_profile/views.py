# coding: utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import json


# Create your views here.
@login_required(login_url="/user/login/")
def favorite(request):
    current_user_profile = UserProfile.objects.filter(user=request.user)
    user_favorite_info = {}
    if current_user_profile:
        user_favorite_info['user_favorite_crawl_media_sort'] = current_user_profile.user_favorite_crawl_media_sort
        user_favorite_info['user_favorite_crawl_media'] = current_user_profile.user_favorite_crawl_media
        user_favorite_info['user_favorite_crawl_dir_sort'] = current_user_profile.user_favorite_crawl_media
    return HttpResponse(json.dumps(user_favorite_info), content_type="application/json")


@login_required(login_url="/user/login/")
def update_favorite(request):
    pass


@login_required(login_url="/user/login/")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/user/login/")