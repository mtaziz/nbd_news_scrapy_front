from django.shortcuts import render
from models import CustomUser
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def favorite(request):
    desc = CustomUser.objects.all()[0]
    return HttpResponse(desc)