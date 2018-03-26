from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 and (postData['first_name'].isalpha() != True):
            errors['first_name'] = 'First name must be at least 2 characters and only letters'
        if len(postData['last_name']) < 2 and (postData['last_name'].isalpha() != True):
            errors['last_name'] = 'Last name must be at least 2 characters and only letters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be valid'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Passwords must match'
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors['doub_email'] = 'Email already in use, please log in' 
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['email'])) < 1:
            errors['wrong_email'] = 'Incorrect email or password' 
        else:
            u = User.objects.get(email=postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), u.password.encode()) != True:
                errors['wrong_password'] = 'Incorrect email or password'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()
