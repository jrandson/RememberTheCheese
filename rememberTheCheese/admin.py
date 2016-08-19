from django.contrib import admin

# Register your models here.

from .models import Lista, Item

admin.site.register(Lista)
admin.site.register(Item)
