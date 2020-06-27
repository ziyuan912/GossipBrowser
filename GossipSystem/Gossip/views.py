from django.shortcuts import render
from django.http import HttpResponseRedirect
from Gossip.models import user, document, recommend_doc
import json

import sys
sys.path.insert(1, '../')
import vsm.doc_ranking as vd
from random import sample

idf, vocab, center, cluster_vector, cluster_id = vd.load_model()

def get_recommend_set(user):
    recommend_set = list(recommend_doc.objects.filter(user__account = user.account))
    #recommend_set = list(recommend_doc.objects.all())
    result = []
    if len(recommend_set) == 0:
        result = [1, 2, 3, 4, 5]
        return result
    else:
        rand_set = sample(recommend_set, 5)
        for doc in rand_set:
            result.append(doc.document)
        return result

def get_doc_list(documents):
    doc_list = []
    for doc in documents:
            f = open("Gossip/templates/article_htmls/" + str(doc) + ".html")
            context = f.read()
            topic = context.split('<h1 class="major">')[1].split('</h1>')[0]
            doc_list.append(document(ID=doc, topic=topic))
            f.close()
    return doc_list

def login(request):
    """if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')"""
    username = request.POST.get('Account', '')
    password = request.POST.get('Password', '')
    User = user.objects.filter(account = username).filter(password = password).first()
    if User is not None:
        #auth.login(request, user)

        recommend_set = get_recommend_set(User)
        rec_list = get_doc_list(recommend_set)
        return render(request, 'welcome.html', {'username': User, 'documents': [], 'recommends': rec_list})
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
    User = user.objects.filter(account = username).first()
    recommend_set = get_recommend_set(User)
    rec_list = get_doc_list(recommend_set)
    if query == '':
        return render(request, 'welcome.html', {
            'username': User, 'documents': json.dumps([]), 'recommends': rec_list
        })
    else:
        documents = vd.cal(query, idf, vocab, center, cluster_vector, cluster_id)
        documents, recommend = documents[:10], documents[10:]
        for rec in recommend:
            recommend_object = recommend_doc(user=User, document=rec)
            recommend_object.save()       
        doc_list = get_doc_list(documents) 
        return render(request, 'welcome.html', {
            'username': User, 'documents': doc_list, 'recommends': rec_list
        })

def document_details(request, docid):
    return render(request, 'article_htmls/' + str(docid) + '.html')
