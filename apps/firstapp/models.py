from __future__ import unicode_literals

from django.db import models
from datetime import datetime

class Users(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    birthday = models.DateField('date_created')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Appointments(models.Model):
    task = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    time = models.DateTimeField('date_created')
    user = models.ForeignKey(Users, related_name = "user_appointments")
