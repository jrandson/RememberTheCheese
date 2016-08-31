from django.test import TestCase

# Create your tests here.

import datetime

from django.utils import timezone
from django.test import TestCase 

from .models import Task,SubTask

from django.core.urlresolvers import reverse
from django.test import Client
from django.test.utils import setup_test_environment

class TaskMethodTest(TestCase):


	def setup(self):
		pass


	def test_description_should_not_be_blank(self):
		
		self.assertEqual(None, None)

	def test_shoud_rate_task_completed(self):
		task = Task.objects.create(description = 'task teste')				
		subtask1 = SubTask.objects.create(task = task)
		
		
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
		task = Task.objects.create(
			description = 'task friendly deadline', 
			deadline = timezone.now()			
		)
		self.assertEqual('Today', task.get_deadline())

		task = Task.objects.create(
			description = 'task friendly deadline', 
			deadline= timezone.now() + datetime.timedelta(days = 1)
		)
		self.assertEqual('Tomorrow', task.get_deadline())

		task = Task.objects.create(
			description = 'task friendly deadline', 
			deadline= timezone.now() - datetime.timedelta(days = 1)
		)
		self.assertEqual('Yesterday', task.get_deadline())

		task = Task.objects.create(
			description = 'task friendly deadline', 
			deadline= timezone.now() - datetime.timedelta(days = 2)
		)
		self.assertEqual('2 days ago', task.get_deadline())

		task = Task.objects.create(
			description = 'task friendly deadline', 
			deadline= timezone.now() + datetime.timedelta(days = 2)
		)
		self.assertEqual('In 2 days', task.get_deadline())

		task.deadline = timezone.now() + datetime.timedelta(days = 4)
		task.save()
		self.assertEqual((timezone.now() + datetime.timedelta(days = 4)).date(), task.get_deadline().date())

class TasksViewsTest(TestCase):

	base_url = 'http://localhost:8000/rememberTheCheese/'

	def setUp(self):
		self.client = Client()
		self.task1 = Task.objects.create(description = 'integration task ')
		self.subtask1 = SubTask.objects.create(
			description = 'integrayion subtask',
			task = self.task1
		)		

	def test_index_should_be_ok(self):	
		
		response = self.client.get(self.base_url)
		self.assertEqual(200,response.status_code)

	def test_should_create_a_valid_task(self):
		qtd_tasks_before = Task.objects.all().count()		
		
		response = self.client.post(self.base_url + 'create_task/', {'description' : 'a new task'})
		self.assertEqual(302,response.status_code)
		
		qtd_tasks_after = Task.objects.all().count()
		
		self.assertEqual(qtd_tasks_before + 1, qtd_tasks_after)


	def test_should_not_create_a_invalid_task(self):
		
		qtd_tasks_before = Task.objects.all().count()		
		
		response = self.client.post(self.base_url + 'create_task/', {'description' : ''})
		self.assertEqual(200,response.status_code)
		#self.assertEqual(self.base_url, response['Location'])
		
		qtd_tasks_after = Task.objects.all().count()
		
		self.assertEqual(qtd_tasks_before, qtd_tasks_after)
	
	def test_do_not_should_create_a_blank_subtask(self):
		task = Task.objects.create()
		subtask = SubTask.objects.create(task = task)	

		response = self.client.get(self.base_url+'detail_task/subtask', {'subtask_id' : subtask.id})
		self.assertEqual(404, response.status_code)

	def test_subtask_for_today_should_be_ok(self):
		
		response = self.client.get(self.base_url+ 'subtasks_for_today/')
		self.assertEqual(200, response.status_code)

	def test_create_task_should_be_ok(self):	
		response = self.client.get(self.base_url+ 'create_task/')
		self.assertEqual(200, response.status_code)

	def test_update_task_should_be_ok(self):		
		task = Task.objects.create(description = 'teste')
		subtask = SubTask.objects.create(description = 'teste', task = task)

		response = self.client.get(self.base_url+'update_task/' + str(task.id))
		self.assertEqual(301, response.status_code)

	def test_detail_task_should_be_ok(self):	

		task = Task.objects.create(description = 'teste')
		subtask = SubTask.objects.create(description = 'teste', task = task)

		response = self.client.get(self.base_url+'detail_task/' + str(task.id))
		self.assertEqual(301,response.status_code)

