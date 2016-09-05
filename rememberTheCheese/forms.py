from django import forms

from rememberTheCheese.models import Task, SubTask

class TaskForm(forms.ModelForm):
	
	class Meta:
		model = Task
		fields = [
			"description",	
			"deadline",		
		]

class SubTaskForm(forms.ModelForm):
	
	class Meta:
		model = SubTask
		fields = [
			"description",	
			"deadline",
		]

