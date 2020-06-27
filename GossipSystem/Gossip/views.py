from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import user, document
import json

import sys
sys.path.insert(1, '../')
import vsm.doc_ranking as vd

idf, vocab, center, cluster_vector, cluster_id = vd.load_model()

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
        documents = vd.cal(query, idf, vocab, center, cluster_vector, cluster_id)
        # documents = [0, 1, 2, 3, 4]
        doc_list = []
        for doc in documents:
            f = open("Gossip/templates/article_htmls/" + str(doc) + ".html")
            context = f.read()
            topic = context.split('<h1 class="major">')[1].split('</h1>')[0]
            doc_list.append(document(ID=doc, topic=topic))
            f.close()
        return render(request, 'welcome.html', {
            'username': username, 'documents': doc_list
        })

def document_details(request, docid):
    return render(request, 'article_htmls/' + str(docid) + '.html')
