from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import user

def login(request):
    """if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')"""
    username = request.POST.get('Account', '')
    password = request.POST.get('Password', '')
    User = user.objects.filter(account = username).filter(password = password).first()
    if User is not None:
        #auth.login(request, user)
        return HttpResponseRedirect('/index/')
    elif username == '' and password == '':
        return welcome(request, username, 1)
    else:
        return welcome(request, username, 0)

def index(request):
    return render(request, 'index.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')

def welcome(request, username, account_exist):
    return render(request, 'welcome.html', {
        'username': username, 'account_exist': account_exist
    })
