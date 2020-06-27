from django.shortcuts import render
from django.http import HttpResponseRedirect
#from .models import user
import json

for i in range(10):
	f = open("templates/article_htmls/" + str(i) + ".html")
	context = f.read()
	topic = context.split('<h1 class="major">')[1].split('</h1>')[0]
	print(topic)