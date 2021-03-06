from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


import math

# Create your models here.

def label_date(deadline):

	if deadline.date() == timezone.now().date():
		return 'Today'

	if deadline.date() == (timezone.now() + datetime.timedelta(days=1)).date():
		return 'Tomorrow'

	if deadline.date() == (timezone.now() - datetime.timedelta(days=1)).date():
		return 'Yesterday'

	dt = (deadline.date() - timezone.now().date()).days

	if abs(dt) < 3:
		if dt < 0:
			return str(abs(dt)) + " days ago"
		else:
			return "In " + str(abs(dt)) + " days"

	return deadline

class TaskList(models.Model):

	description = models.CharField(max_length=100, null=False)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	modified_at = models.DateTimeField(auto_now=True, editable=False)

	def get_priority_projects(self):
		return TaskList.objects.filter(priority=1)[0:3]

	def setTask(self):
		tasks = Task.objects.all()
		tasklist = TaskList.objects.get(description='Inbox')
		for task in tasks:
			task.tasklist = tasklist
			task.save()

class Task(models.Model):
	description = models.CharField(max_length=500, null=False)
	deadline = models.DateTimeField('deadline', default=timezone.now()+ datetime.timedelta(days=3))
	finished = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	modified_at = models.DateTimeField(auto_now=True, editable=False)
	closed = models.IntegerField(default = 0)
	started = models.IntegerField(default = 0)
	observation = models.TextField(blank = True)
	tasklist = models.ForeignKey(TaskList, on_delete = models.CASCADE)

	def __str__(self):
		return self.description

	def get_all_subtasks(self):
		subtask = SubTask()
		subtasks = subtask.objects.get(task = self)

		return subtasks

	def get_created_at(self):
		return label_date(self.created_at)

	def get_modified_at(self):
		return label_date(self.modified_at)

	def get_deadline(self):
		return label_date(self.deadline)

	def get_unfinished_subtasks(self):
		return self.subtask_set.filter(finished=0).order_by('-created_at')

	def get_finished_subtasks(self):
		return self.subtask_set.filter(finished=1, task_id = self.id).order_by('-modified_at')

	def get_closed_tasks(self):
		return Task.objects.filter(closed=1).order_by('-modified_at')

	def get_tasks_for_today(self):
		tasks = Task.objects.filter(finished=0).order_by('-created_at')		
		tasks_for_today = []
		
		for task in tasks:
			if task.is_for_today():
				tasks_for_today.append(task)

		return tasks_for_today

	def group_task_by_tasklist(self,tasks):
		pass

	

	def search(self, search):

		tasks = Task.objects.filter(description__icontains = search)
		return tasks

	def get_pct_finished(self):

		all_tasks = self.subtask_set.all().count()

		if all_tasks == 0:
			return 0

		finished_tasks = self.subtask_set.filter(finished=1).count()

		return round(100.0*finished_tasks/all_tasks);

	def get_qtd_subtasks(self):
		return self.subtask_set.all().count()

	def get_tasks_inbox(self):

		tasks = Task.objects.filter(closed = 0).order_by('-created_at')

		return tasks

	def is_for_today(self):	
		return self.get_deadline() == 'Today'

	def is_late(self):
		
		if self.is_for_today():
			return False

		return self.deadline < timezone.now()

	def get_started_task(self):
		return Task.objects.filter(started=1, finished = 0)

	

class SubTask(models.Model):
	"""docstring for subtasks"""
	task = models.ForeignKey(Task, on_delete = models.CASCADE)
	description = models.CharField(max_length=100, null=False)
	deadline = models.DateTimeField('deadline', default=timezone.now() + datetime.timedelta(days=3))
	finished = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	modified_at = models.DateTimeField(auto_now=True, editable=False)

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

q.choice_set.all()
'''




