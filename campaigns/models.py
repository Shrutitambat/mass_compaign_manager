from django.db import models
from django.contrib.auth.models import User


class ContactList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_lists')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    contact_list = models.ForeignKey(ContactList, on_delete=models.CASCADE, related_name='subscribers')
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('contact_list', 'email')

    def __str__(self):
        return f"{self.email} ({self.contact_list.name})"