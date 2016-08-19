# -* - coding:utf8 -*- 

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from rememberTheCheese.models import Lista, Item
from django.shortcuts import render, get_object_or_404,redirect
from django.core.urlresolvers import reverse
from django.views import generic

# Create your views here.

def index(request):
	
	context = {
		'tasks' : Lista.objects.all()
	}
	#template = loader.get_template('rememberTheCheese/index.html')
	#return HttpResponse(template.render(context,request))
	return render(request, 'rememberTheCheese/index.html', context)

def create(request, task_id):
	task = get_object_or_404(Lista, pk = task_id)

	try:
		item = Item()
		item.description = request.POST['description']
		item.lista = task
		item.save()

		return HttpResponseRedirect(reverse('detail', args = (task.id,)))		

	except(KeyError, Item.DoesNotExist):
		return render(request, 'rememberTheCheese/detail.html/'+str(task.id),{
			'lista': task,
			'error_message' : "subtask description could'nt be blank",
			})

def delete(request, item_id):

	item = get_object_or_404(Item, pk=item_id)
	task_id = item.lista.id
	item.delete()

	return redirect('detail', task_id=task_id)

def edit(request, id_item):
	pass

def update(request):
	pass

def detail(request, task_id):
	response = "These are your tasks"
	# get_list_or_404() 
	lista = get_object_or_404(Lista, pk=task_id)
	context = {
		'lista' : Lista.objects.get(pk=task_id)
	}
	return render(request,'rememberTheCheese/detail.html',context)

def tasks_for_today(request):
	response = "You have to finish this tasks today "
	return HttpResponse(response)

def get_task(request, task_list_id):
	task = Lista()
	items = task.get_all_items()

	context = {
		'items': items
	}

	return render(request,'rememberTheCheese/items.html', context)

def detail_item(request,item_id):
	
	item = Item()

	context = {
		'item' : item.findByPk(item_id)
	}
	#return HttpResponse(response % item_id)
	return render(request, 'rememberTheCheese/detail_item.html',context)

