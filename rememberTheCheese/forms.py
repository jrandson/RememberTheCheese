from django import forms

from rememberTheCheese.models import *

class CreateTask(forms.ModelForm):
	class Meta:
		model = Task
		fields = [
			"description",			
		]