from django.db import models

# Create your models here.
class user(models.Model):
	account = models.CharField(max_length=50, help_text='account')
	password = models.CharField(max_length=50, help_text='password')

class document():
	def __init__(self, ID, topic):
	        self.ID = ID
	        self.topic = topic

class recommend_doc(models.Model):
	user = models.ForeignKey(user, on_delete=models.CASCADE)
	document = models.IntegerField()
		
