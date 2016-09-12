from django.contrib import admin

# Register your models here.

from .models import Task, SubTask, TaskList

admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(TaskList)
