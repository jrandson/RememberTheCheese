# -* - coding:utf8 -*- 

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from rememberTheCheese.models import Task,SubTask
from django.shortcuts import render, get_object_or_404,redirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib import messages

from django.utils import timezone

from .forms import CreateTask

# Create your views here.

def teste(request):

	response = "teste"
	task = Task.objects.get(pk=4)

	return HttpResponse(task.get_pct_finished())

def index(request):

	taskModel = Task()
	if 'search' in request.POST.keys() and request.POST['search'] != '':
		tasks = taskModel.search(request.POST['search'])
	else:
		tasks = Task.objects.all()[:10]

	context = {
		'tasks' : tasks,	
		'form' :  CreateTask(request.POST or None)
	}

	#template = loader.get_template('rememberTheCheese/index.html')
	#return HttpResponse(template.render(context,request))
	return render(request, 'rememberTheCheese/index.html', context)

def subtasks_for_today(request):
	task = Task()
	subtasks = task.get_subtasks_for_today()
	context = {
		'subtasks' : subtasks
	}

	return render(request,'rememberTheCheese/subtasks_for_today.html',context)


#=================tasks=======================================

def create_task(request):
	
	form = CreateTask(request.POST or None)

	context = {
		'form' : form
	}

	if form.is_valid():
		desc = request.POST['description']
		task = Task(description= desc)
		task.save()

		messages.success(request,'Successfully created')
		return redirect('index')

	return render(request, 'rememberTheCheese/create_task.html',context)


def update_task(request, task_id=None):
	task = get_object_or_404(Task, id=task_id)
	form = CreateTask(request.POST or None, instance=task)
	if form.is_valid():
		desc = request.POST['description']
		task = Task(description= desc)
		task.save()

		messages.success(request,'Successfully created')

	context = {
		'description' : task.description,
		'form' : form
	}

	return render(request, 'rememberTheCheese/update_task.html',context)

def detail_task(request, task_id):
	response = "These are your tasks"
	# get_list_or_404() 
	task = get_object_or_404(Task, pk=task_id)
	
	context = {
		'task' : task
	}

	return render(request,'rememberTheCheese/detail_task.html',context)

def delete_task(request,task_id):
	task = get_object_or_404(Task, pk=task_id)
	task.delete()

	return redirect('index')


#====================subtasks=======================================


def create_subtask(request, task_id):
	task = get_object_or_404(Task, pk = task_id)

	try:
		subtask = SubTask()
		subtask.description = request.POST['description']
		subtask.task = task
		subtask.save()

		return HttpResponseRedirect(reverse('detail_task', args = (task.id,)))		

	except(KeyError, SubTask.DoesNotExist):
		return render(request, 'rememberTheCheese/detail.html/'+str(task.id),{
			'task': task,
			'error_message' : "subtask description could'nt be blank",
			})

def delete_subTask(request, subTask_id):

	subtask = get_object_or_404(SubTask, pk=subTask_id)
	task_id = subtask.task.id
	subtask.delete()

	return HttpResponseRedirect(reverse('detail_task', args = (task_id,)))



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

	subtasks = request.POST['subtasks']
	task_id = request.POST['task_id']

	for subtask_id in subtasks:
		subtask = SubTask.objects.get(pk=subtask_id)
		subtask.finished = 1
		subtask.save()

	return HttpResponseRedirect(reverse('detail_task', args = (task_id,)))

#============================================================================