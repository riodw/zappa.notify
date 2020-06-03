import uuid
from django.db import models



def keyGen():
	d = str(uuid.uuid4())
	return d.replace('-','')


class StringKeyGenerator(object):
	def __init__(self, len=16):
		self.lenght = len
	def __call__(self):
		return ''.join(random.choice(string.letters + string.digits) for x in range(self.lenght))


# Create your models here.
class Notification(models.Model):
	# Fields
	public_id = models.CharField(
		max_length=32,
		editable=False,
		unique=True,
		default=keyGen,
	)
	subject = models.CharField(
		max_length=254,
		default='Notify Notification',
	)
	message = models.TextField()
	datetime = models.DateTimeField(
		auto_now_add=True,
		blank=True,
	)
	created_date = models.DateTimeField(
		auto_now_add=True,
	)
	recipient = models.EmailField(
		max_length=255,
	)
	# What email address is sending the email
	sender = models.EmailField(
		max_length=254,
	)
	# What application did this notification get created from?
	source = models.CharField(
		max_length=254,
	)
	type = models.IntegerField(
		default=0,
	)
	runs = models.IntegerField(
		default=0,
	)
	sent = models.BooleanField(
		default=False,
	)
	active = models.BooleanField(
		default=True,
	)

	class Meta:
		ordering = ['datetime']