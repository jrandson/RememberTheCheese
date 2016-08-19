from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Lista(models.Model):
	description = models.CharField(max_length=500, blank=False)
	date_create = models.DateTimeField('date created')
	deadline = models.DateTimeField('deadline', default=timezone.now() + datetime.timedelta(days=15))

	def __str__(self):
		return self.description


	def get_all_items(self):
		item = Item()
		items = item.objects.get(lista = self)

		return items

class Item(models.Model):
	"""docstring for Item"""
	lista = models.ForeignKey(Lista, on_delete = models.CASCADE)
	description = models.CharField(max_length=500, blank = False)
	deadline = models.DateTimeField('deadline', default=timezone.now() + datetime.timedelta(days=3))
	finished = models.IntegerField(default=0)

	def __str__(self):
		return self.description

	def list_all_for_today(self):
		return self.date_create > timezone.now() - datetime.timedelta(days=1)

	def findByPk(self, item_id):
		return Item.objects.get(pk = item_id)




	'''
	Question.objects.all()
	Question.objects.get(pk=1)
	Question.objects.get(id=2)
	Question.objects.filter(id=1)
	Question.objects.filter(question_text__startswith='What')
	q.[choice]_set.all()
	Question.objects.get(pub_date__year=current_year)
	'''

		

