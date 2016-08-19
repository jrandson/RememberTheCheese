from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<task_id>[0-9]+)/$', views.detail, name='detail'),   
    url(r'^tasks_for_today/$', views.tasks_for_today, name='tasks_for_today'),
    # ex: rememberTheCheese/5/
    url(r'^get_task/(?P<task_list_id>[0-9]+)/$',views.get_task, name='get_task'),
    # ex: rememberTheCheese/5/items
    url(r'^detail_item/(?P<item_id>[0-9]+)/items/$',views.detail_item, name='item_detail'),
    url(r'^create/(?P<task_id>[0-9]+)/$',views.create, name='create'),

    url(r'^delete/(?P<item_id>[0-9]+)/$',views.delete,name='delete'),
    url(r'^edit/(?P<item_id>[0-9]+)/$',views.edit,name='edit'),
    url(r'^delete/(?P<item_id>[0-9]+)/$',views.update,name='update'),
]