from django.contrib import admin

# Register your models here.

from .models import ContactList, Subscriber

admin.site.register(ContactList)
admin.site.register(Subscriber)
