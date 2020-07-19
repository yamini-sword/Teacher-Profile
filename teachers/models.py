from django.db import models

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    email = models.EmailField(max_length=254, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=100)
    #first_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    room_number = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.email
