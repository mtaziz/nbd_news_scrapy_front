from django.shortcuts import render, HttpResponse
from models import UserProfile, User
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def favorite(request):
    current_user = request.user
    # desc = User.objects.all()[0].get_profile().description
    return HttpResponse(current_user)