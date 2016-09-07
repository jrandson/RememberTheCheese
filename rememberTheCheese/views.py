# -* - coding:utf8 -*- 

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from django.core.urlresolvers import reverse
from django.views import generic

from rememberTheCheese.models import Task,SubTask

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.utils import timezone

from .forms import TaskForm, SubTaskForm, UserForm, ContactForm



# Create your views here.

base_url = 'rememberTheCheese/'

def teste(request):

	return HttpResponse('No tasks are available')

#@login_required(redirect_field_name='my_redirect_field', login_url='/accounts/login/')
def index(request):

	print 'request', request
	if not request.user.is_authenticated:
		pass


	if request.user.is_authenticated():
		title = "Hello %s" % (request.user)

	taskModel = Task()

	if 'search' in request.POST.keys() and request.POST['search'] != '':
		tasks = taskModel.search(request.POST['search'])
	else:
		tasks = taskModel.get_tasks_inbox()[:10]

	context = {

		'tasks' : tasks,
		'tasks_inbox' : taskModel.get_tasks_inbox(),
		'form' :  TaskForm(request.POST or None)
	}

	#template = loader.get_template('rememberTheCheese/index.html')
	#return HttpResponse(template.render(context,request))
	#return HttpResponse("Welcome")
	return render(request,'rememberTheCheese/index.html', context)

def today(request):
	task = Task()
	tasks = task.get_tasks_for_today()

	context = {
		'tasks' : tasks
	}
	
	return render(request,'rememberTheCheese/today.html',context)

def not_found(request):
	context = {

	}
	return render(request,'rememberTheCheese/404.html',context)

def internal_error(request):
	context = {

	}
	return render(request,'rememberTheCheese/500.html', context)

def auth_login(request):
	
	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		
		user = authenticate(username=username, password=password)
		
		if user is not None:
			login(request, user)
			return redirect('rememberTheCheese:index')
		else:
			return redirect('rememberTheCheese:login')

	return render(request,'rememberTheCheese/login.html',{})

def auth_logout(request):
	logout(request)
	return redirect(request,'rememberTheCheese',{})

def auth_register(request):
	form = UserForm(request.POST or None)
	context = {
		'form': form
	}

	if form.is_valid():

		instance = form.save(commit= False)
		instance.save()
		messages.success(request,'User successfully created')
		
		return redirect('rememberTheCheese:index')

	return render(request, 'rememberTheCheese/register.html',context)

	

def create_task(request):	
	#return HttpResponse(request.POST['deadline'])
	form = TaskForm(request.POST or None)
	context = {
		'form' : form
	}

	if form.is_valid():
		#desc = request.POST['description']
		instance = form.save(commit=False)
		instance.save()		

		messages.success(request,'Successfully created')
		print 'status code', HttpResponse.status_code		
		return redirect('rememberTheCheese:index')

	return render(request, base_url+'create_task.html',context)

def users(request):

	users = User.objects.all()

	context = {
		'users' : users,
	}

	return render(request, 'rememberTheCheese/users.html', context)

def update_task(request, task_id=None):
	
	task = get_object_or_404(Task, id=task_id)
	form = TaskForm(request.POST or None, instance = task)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()		

		messages.success(request,'Task updated successfully')

		return redirect('rememberTheCheese:index')	

	context = {
		'task' : task,
		'form' : form
	}

	return render(request, base_url+'update_task.html',context)

def close_task(request, task_id):	

	task = Task.objects.get(pk = task_id)
	task. closed = 1
	task.save()

	return redirect('rememberTheCheese:index')

def detail_task(request, task_id):
	response = "These are your tasks"

	# get_list_or_404() 
	task = get_object_or_404(Task, pk=task_id)
	
	form = SubTaskForm(request.POST or None)
	context = {
		'task' : task,
		'form': form,
		'finished_subtasks': task.get_finished_subtasks(),
		'unfinished_subtasks' : task.get_unfinished_subtasks()
	}

	return render(request, base_url+'detail_task.html',context)

def delete_task(request,task_id):
	task = get_object_or_404(Task, pk=task_id)
	task.delete()

	return redirect('rememberTheCheese:index')

def undo_finished_subtasks(request):

	if request.method == 'POST' and request.POST.getlist('finished_subtasks'):
		finished_subtasks = request.POST.getlist('finished_subtasks')
		
		for subTask_id in finished_subtasks:
			subtask = get_object_or_404(SubTask, pk=subTask_id)
			subtask.finished = 0
			subtask.save()

			task_id = subtask.task_id

		return HttpResponseRedirect(reverse('detail_task', args = (task_id,)))

	return redirect('rememberTheCheese:index')

def create_subtask(request, task_id):
	task = get_object_or_404(Task, pk = task_id)

	
	form = SubTaskForm(request.POST or None)

	if form.is_valid() :
		instance = form.save(commit = False)
		instance.task = task
		instance.save()

		messages.success(request,'Subtask created successfully')

		return HttpResponseRedirect(reverse('rememberTheCheese:detail_task', args = (task.id,)))

	context = {
		'form' : form,
		'task': task,
	}
	return render(request, 'rememberTheCheese/detail_task.html', context)		

def delete_subTask(request, subTask_id):

	subtask = get_object_or_404(SubTask, pk=subTask_id)
	task_id = subtask.task.id
	subtask.delete()

	return HttpResponseRedirect(reverse('rememberTheCheese:detail_task', args = (task_id,)))

def edit(request, id_subtask):
	passs	

def get_task(request, task_list_id):
	task = Task()
	subtasks = task.get_all_subtasks()

	context = {
		'subtasks': subtasks
	}

	return render(request,'rememberTheCheese/subtask.html', context)

def detail_subTask(request,subTask_id):
	
	subtasks = SubTask()

	context = {
		'subtask' : subtasks.findByPk(subTask_id)
	}
	#return HttpResponse(response % subtasks_id)
	return render(request, 'rememberTheCheese/detail_subTask.html',context)

def mark_subtask_as_finished(request):

	if request.method == 'POST':

		subtasks = request.POST.getlist('subtasks')
		task_id = request.POST['task_id']

		for subtask_id in subtasks:
			subtask = get_object_or_404(SubTask, pk = int(subtask_id))
			subtask.finished = 1
			subtask.save()

	return HttpResponseRedirect(reverse('rememberTheCheese:detail_task', args = (task_id,)))

#============================================================================