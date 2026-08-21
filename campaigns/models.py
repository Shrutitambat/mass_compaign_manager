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




class EmailTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='templates')
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=255)
    body = models.TextField(help_text="Use placeholders like {{name}} for dynamic tags.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('READY', 'Ready'),
        ('QUEUED', 'Queued'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=200)
    contact_list = models.ForeignKey(ContactList, on_delete=models.CASCADE, related_name='campaigns')
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, related_name='campaigns')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='DRAFT')
    sent_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"