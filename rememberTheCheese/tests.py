from django.test import TestCase

# Create your tests here.

import datetime

from django.utils import timezone
from django.test import TestCase 

from .models import Task,SubTask

from django.core.urlresolvers import reverse

class TaskMethodTest(TestCase):

	def test_description_should_not_be_blank(self):
		task = Task()
		task.save()
		self.assertEqual(None, None)

	def test_shoud_rate_task_completed(self):
		task = Task(description = 'task teste')
		task.save()
		
		subtask1 = SubTask(task = task)
		subtask1.save()
		
		subtask2 = SubTask(task = task)
		subtask2.save()
		
		subtask3 = SubTask(task = task)
		subtask3.save()

		self.assertEqual(0, task.get_pct_finished())

		subtask1.finished = 1
		subtask1.save()

		self.assertEqual(100*round(1.0/3,2), task.get_pct_finished())

		subtask2.finished = 1
		subtask2.save()

		self.assertEqual(100*round(2.0/3, 2), task.get_pct_finished())

		subtask3.finished = 1
		subtask3.save()

		self.assertEqual(100 , task.get_pct_finished())
	
	def test_show_frinfly_deadline(self):
		task = Task(description = "teste", deadline = timezone.now())
		task.save()
		self.assertEqual('Today', task.get_deadline())

		task.deadline = timezone.now() + datetime.timedelta(days = 1)
		task.save()
		self.assertEqual('Tomorrow', task.get_deadline())

		task.deadline = timezone.now() - datetime.timedelta(days = 1)
		task.save()
		self.assertEqual('Yesterday', task.get_deadline())

		task.deadline = timezone.now() - datetime.timedelta(days = 2)
		task.save()
		self.assertEqual('2 days ago', task.get_deadline())

		task.deadline = timezone.now() + datetime.timedelta(days = 2)
		task.save()
		self.assertEqual('In 2 days', task.get_deadline())

		task.deadline = timezone.now() + datetime.timedelta(days = 4)
		task.save()
		self.assertEqual((timezone.now() + datetime.timedelta(days = 4)).date(), task.get_deadline().date())



class TasksViewsTest(TestCase):

	def test_index_view_with_no_tasks(self):
		pass
		"""response = self.client.get(reverse('rememberTheCheese:index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, 'No tasks are available.')
		self.assertQuerysetEqual(response.context['tasks'],[])"""

