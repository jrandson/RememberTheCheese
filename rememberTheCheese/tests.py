from django.test import TestCase

# Create your tests here.

import datetime

from django.utils import timezone
from django.test import TestCase 

from .models import Task,SubTask

class TaskMethodTest(TestCase):

	def test_description_should_not_be_blank(self):
		task = Task()
		task.save()
		self.assertEqual(None, task.description)


