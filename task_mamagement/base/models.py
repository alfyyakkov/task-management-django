from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    assigned_to = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='users', null= True, blank= True)

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tasks', null= True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.FloatField(blank=True, null=True)
