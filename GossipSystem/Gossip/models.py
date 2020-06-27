from django.db import models

# Create your models here.
class user(models.Model):
	account = models.CharField(max_length=50, help_text='account')
	password = models.CharField(max_length=50, help_text='password')

class document(models.Model):
	ID = models.IntegerField()
	topic = models.CharField(max_length=100, help_text='topic')
