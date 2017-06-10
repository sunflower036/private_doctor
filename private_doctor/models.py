from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Doctor(models.Model):
    user = models.CharField(max_length=32, primary_key=True)
    pwd = models.CharField(max_length=32)
    sex = models.CharField(max_length=32)
    email = models.CharField(max_length=32)

class Family(models.Model):
    user = models.CharField(max_length=32, primary_key=True)
    pwd = models.CharField(max_length=32)
    sex = models.CharField(max_length=32)
    email = models.CharField(max_length=32)

class Appointment(models.Model):
    family = models.ForeignKey(Family)
    doctor = models.ForeignKey(Doctor)
    time = models.DateField()
    
class Family_Doctor(models.Model):
    family = models.ForeignKey(Family)
    doctor = models.ForeignKey(Doctor)

class DoctorInfo(models.Model):
    doctor = models.ForeignKey(Doctor)
    text = models.TextField()

