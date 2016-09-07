from django import forms

from rememberTheCheese.models import Task, SubTask
from django.contrib.auth.models import User

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
class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username',"email", 	"password", "first_name", "last_name",]
		#fields = '__all__'


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
