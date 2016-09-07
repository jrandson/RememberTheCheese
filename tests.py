import datetime

from django.utils import timezone 

from .models import Task,SubTask

from django.core.urlresolvers import reverse

from django.test import Client
from django.test.utils import setup_test_environment
from django.test import TestCase

from .forms import UserForm

from django.contrib.auth.models import User

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
	
	def test_show_friendly_deadline(self):
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

	def test_dead_line_is_today(self):		
		task = Task.objects.create(description="task",deadline=timezone.now())
		self.assertEqual(True,task.is_for_today())

		task.deadline = timezone.now() + datetime.timedelta(days = 1)
		task.save()
		self.assertEqual(False,task.is_for_today())

		task.deadline = timezone.now() - datetime.timedelta(days = 1)
		task.save()
		self.assertEqual(False,task.is_for_today())

		task.deadline = timezone.now() + datetime.timedelta(days = 10)
		task.save()
		self.assertEqual(False,task.is_for_today())

		task.deadline = timezone.now() - datetime.timedelta(days = 12)
		task.save()
		self.assertEqual(False,task.is_for_today())

	def test_id_for_today(self):
		
		task = Task.objects.create(description = 'task', deadline= timezone.now() + datetime.timedelta(days=1))
		self.assertEqual(False,task.is_for_today())

		task = Task.objects.create(description = 'task', deadline= timezone.now())
		self.assertEqual(True,task.is_for_today())

		task = Task.objects.create(description = 'task', deadline= timezone.now() - datetime.timedelta(days=1))
		self.assertEqual(False,task.is_for_today())
	
	def test_is_late(self):
		task = Task.objects.create(description = 'task', deadline= timezone.now() - datetime.timedelta(days=1))
		self.assertEqual(True, task.is_late())

		task = Task.objects.create(description = 'task', deadline= timezone.now())
		self.assertEqual(False, task.is_late())

		task = Task.objects.create(description = 'task', deadline= timezone.now() + datetime.timedelta(days=1))
		self.assertEqual(False, task.is_late())


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
		
		response = self.client.post(
			self.base_url + 'create_task/'
		)
		self.assertEqual(200,response.status_code)

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

	def test_task_for_today(self):
		task1 = Task.objects.create(description='task 1', deadline = timezone.now() + datetime.timedelta(days=1))
		task2 = Task.objects.create(description='task 2', deadline = timezone.now() - datetime.timedelta(days=1))
		
		task_for_today = task1.get_tasks_for_today()
		
		response = self.client.get('http://localhost/rememberTheCheese/today/')		
		self.assertEqual(200, response.status_code)
		self.assertEqual(0,len(response.context['tasks']))
		
		task3 = Task.objects.create(description='task 3', deadline = timezone.now())
		self.assertEqual(True, task3.is_for_today())
		
		response = self.client.get('http://localhost/rememberTheCheese/today/')	
		self.assertEqual(1, len(response.context['tasks']))

	def test_should_create_user(self):
		data = {
			'username' : 'username',
			"email" : 'user@email.com', 	
			"password": 'abc@123', 
			"first_name" : 'foo', 
			"last_name" : 'bar',
		}

		form = UserForm({})
		self.assertEqual(False,form.is_valid())
		form = UserForm(data)
		self.assertEqual(True,form.is_valid())

		form.save()
		self.assertEqual({},form.errors)

		data = {
			'username' : 'username',
			"email" : 'user@email.com', 	
			"password": 'abc@123', 
			"first_name" : 'foo', 
			"last_name" : 'bar',
		}

		form = UserForm({})
		self.assertEqual(False,form.is_valid())
		form = UserForm(data)
		self.assertEqual(False,form.is_valid())

		form.save()
		self.assertEqual({},form.errors)

		#response = self.client.get(self.base_url+'update_task/' + str(task.id))

