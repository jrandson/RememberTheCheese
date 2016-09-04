
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static

from . import views

from .views import (
     index,
     teste,
    )

app_name = 'rememberTheCheese'
urlpatterns = [
    #tasks
    url(r'^$', views.index, name='index' ),
    url(r'^teste/$', views.teste),
    url(r'^today/$', views.get_tasks_for_today, name='get_task_for_today'),
    url(r'^subtasks_for_today/$', views.subtasks_for_today, name='subtasks_for_today'),

    #tasks
    url(r'^create_task/$',views.create_task, name='create_task'),
    url(r'^update_task/(?P<task_id>[0-9]+)/$',views.update_task, name='update_task'),
    url(r'^detail_task/(?P<task_id>[0-9]+)/delete_task/$',views.delete_task,name='delete_task'),    
    url(r'^close_task/(?P<task_id>[0-9]+)/$',views.close_task,name='close_task'),
    # ex: rememberTheCheese/5/
    url(r'^get_task/(?P<task_list_id>[0-9]+)/$',views.get_task, name='get_task'),
    url(r'^detail_task/(?P<task_id>[0-9]+)/$', views.detail_task, name='detail_task'),  
    url(r'^undo_finished_subtasks/$', views.undo_finished_subtasks, name='undo_finished_subtasks'), 


    #subtasks   
    
    # ex: rememberTheCheese/5/subtasks
    url(r'^detail_task/subTask/(?P<subTask_id>[0-9]+)/$',views.detail_subTask, name='detail_subTask'),
    url(r'^create_subtask/(?P<task_id>[0-9]+)/$',views.create_subtask, name='create_subtask'),

    url(r'^edit/(?P<subtask_id>[0-9]+)/$',views.edit,name='edit'),
    url(r'^detail_subTask/(?P<subTask_id>[0-9]+)/delete_subTask/$',views.delete_subTask,name='delete_subTask'),
    url(r'^mark_subtask_as_finished/$',views.mark_subtask_as_finished,name='mark_subtask_as_finished'),
]


if settings.DEBUG :
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
