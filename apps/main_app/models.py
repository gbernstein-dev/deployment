from __future__ import unicode_literals
from django.db import models
import bcrypt, datetime

class BlogManager(models.Manager):
  def validator(self, data):
    errors = {}
    for key in data:
      if 'login' in key:
        if len(data['email']) < 3 or len(data['password']) < 3:
          errors['email'] = 'email/password invalid.'
        elif User.objects.filter(email = data['email']).exists() == False:
          errors['email'] = 'email does not exist in database.'
        elif bcrypt.checkpw(data['password'].encode(), User.objects.filter(email = data['email']).first().password.encode()) == False:
          errors['password'] = 'incorrect password.'
      elif 'create' in key:
        if len(data['email']) < 3 or len(data['password']) < 3:
          errors['email'] = 'email/password too short to register.'
        elif len(data['name']) < 3:
          errors['name'] = 'invalid name.'
    return errors

class User(models.Model):
  name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  date_hired = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = BlogManager()

class Product(models.Model):
  product_name = models.CharField(max_length=255)
  creator = models.ForeignKey(User)
  created_at = models.DateTimeField(auto_now_add = True)

class Wish_List(models.Model):
  user = models.ForeignKey(User)
  product = models.ForeignKey(Product)
  created_at = models.DateTimeField(auto_now_add = True)
