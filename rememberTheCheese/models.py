from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

def label_date(date):

	if date == timezone.now():
		return 'Today'

	if date == timezone.now() + datetime.timedelta(days=1):
		return 'Tomorrow'

	if date == timezone.now() - datetime.timedelta(days=1):
		return 'Yesterday'

	return date

class Task(models.Model):
	description = models.CharField(max_length=500)
	date_create = models.DateTimeField('date created', default=timezone.now())
	deadline = models.DateTimeField('deadline', default=timezone.now()+ datetime.timedelta(days=3))
	finished = models.IntegerField(default=0)

	def __str__(self):
		return self.description


	def get_all_subtasks(self):
		subtask = SubTask()
		subtasks = subtask.objects.get(task = self)

		return subtasks

	def get_deadline(self):
		return label_date(self.deadline)

	def get_subtasks_unfinished(self):
		return self.subtask_set.filter(finished=0)

	def get_subtask_finished(self):
		return self.subtask_set.filter(finished=1)

	def get_subtasks_for_today(self):
		query = SubTask.objects.filter(finished=0)
		subtasks = []
		for subtask in query:
			subtasks.append(subtask)
		#deadline = timezone.now().today()
		return subtasks

	def search(self, search):

		tasks = Task.objects.filter(description__icontains = search)
		return tasks

	def get_pct_finished(self):

		all_tasks = Task.objects.all().count()
		finished_tasks = self.subtask_set.filter(finished=1).count()

		return 100.0*finished_tasks/all_tasks;

class SubTask(models.Model):
	"""docstring for subtasks"""
	task = models.ForeignKey(Task, on_delete = models.CASCADE)
	description = models.CharField(max_length=500)
	deadline = models.DateTimeField('deadline', default=timezone.now() + datetime.timedelta(days=3))
	finished = models.IntegerField(default=0)

	def __str__(self):
		return self.description

	def list_all_for_today(self):
		return self.date_create > timezone.now() - datetime.timedelta(days=1)

	def findByPk(self, subTask_id):
		return SubTask.objects.get(pk = subTask_id)

	def get_deadline(self):
		return label_date(self.deadline)

	''' making queries: https://docs.djangoproject.com/en/1.9/topics/db/queries/'''

'''
Question.objects.all()
Question.objects.get(pk=1)
Question.objects.get(id=2)
Question.objects.filter(id=1)
Question.objects.filter(question_text__startswith='What') {__startswith=, __endswith=, __istartswith=, __iendswith=}
q.[choice]_set.all()
Question.objects.get(pub_date__year=current_year)

create and save an object at the same tipe
john = Author.objects.create(name="John")

Entry.objects.filter(pub_date__lte='2006-01-01')
SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';

>>> b = Blog.objects.get(id=1)
>>> b.entry_set.all() # Returns all Entry objects related to Blog.


# b.entry_set is a Manager that returns QuerySets.
>>> b.entry_set.filter(headline__contains='Lennon')
>>> b.entry_set.count()
'''




