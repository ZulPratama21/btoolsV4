from django.db import models

# Create your models here.

class UserDevice(models.Model):
	user	= models.CharField(
		max_length = 100,
		default = 'admin',
		)
	
	password		= models.CharField(max_length = 1000)
	
	listGroup = (
		('Read','read'),
		('Write','Write'),
		('Full','full'),
		)

	group	= models.CharField(
		max_length = 100,
		choices = listGroup,
		default = 'read',
		)
	
	published	= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)

	def __str__(self):
		return "{}. {}".format(self.id,self.user)