# coding: utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, get_object_or_404, _get_queryset
from models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import json
from forms import UserForm, UserProfileForm
from django.contrib import messages


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except AttributeError:
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    except queryset.model.DoesNotExist:
        return {}

# Create your views here.
@login_required(login_url="/user/login/")
def favorite(request):
    current_user_profile = get_object_or_none(UserProfile,user=request.user)
    user_favorite_info = {}
    print current_user_profile
    if  current_user_profile:
        user_favorite_info['user_favorite_crawl_media_sort'] = current_user_profile.user_favorite_crawl_media_sort
        user_favorite_info['user_favorite_crawl_media'] = current_user_profile.user_favorite_crawl_media
        user_favorite_info['user_favorite_crawl_dir_sort'] = current_user_profile.user_favorite_crawl_dir_sort
    return HttpResponse(json.dumps(user_favorite_info), content_type="application/json")


@login_required(login_url="/user/login/")
def update_favorite(request):
    profile_form = UserProfileForm(request.POST, instance=UserProfile.objects.get(user=request.user))
    if profile_form.is_valid():
        profile_form.save()
    return HttpResponse("收藏成功")

@login_required(login_url="/user/login/")
def logout(request):
    auth.logout(request)
    messages.success(request, ('注销成功'))
    return HttpResponseRedirect("/user/login/")

@login_required(login_url="/user/login/")
def help(request):
    return render(request, 'user_profile/help.html')


@login_required(login_url="/user/login/")
def setting(request):
    if request.method == 'POST':
        user_form = UserForm(request.user, request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=UserProfile.objects.get(user=request.user))
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('密码更新成功，请重新登陆'))
            return redirect('user_profile_setting')
        else:
            messages.error(request, ('修正以下错误'))
    else:
        user_form = UserForm(request.user, instance=request.user)
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    return render(request, 'user_profile/setting.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })