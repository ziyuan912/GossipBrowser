from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import user
import json

def login(request):
    """if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')"""
    username = request.POST.get('Account', '')
    password = request.POST.get('Password', '')
    User = user.objects.filter(account = username).filter(password = password).first()
    if User is not None:
        #auth.login(request, user)
        return render(request, 'welcome.html', {'username': User.account, 'documents': []})
    elif username == '' and password == '':
        return render(request, 'login.html', {'account_exist':1})
    else:
        return render(request, 'login.html', {'account_exist':0})

def index(request):
    return render(request, 'index.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')

def welcome(request):
    username = request.POST.get('username')
    query = request.POST.get('Query', '')
    if query == '':
        return render(request, 'welcome.html', {
            'username': username, 'documents': json.dumps([])
        })
    else:
        documents = [0, 1, 2, 3, 4]
        return render(request, 'welcome.html', {
            'username': username, 'documents': documents
        })

def document_details(request, docid):
    return render(request, 'article_htmls/' + str(docid) + '.html')
