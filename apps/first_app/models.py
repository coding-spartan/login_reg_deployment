from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')



class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2 and (postData['name'].isalpha() != True):
            errors['name'] = 'Name must be at least 2 characters and only letters'  
        if len(User.objects.filter(alias=postData['alias'])) > 0 or len(postData['alias']) < 3:
            errors['alias'] = 'Enter a valid alias (Alias is taken or less than 3 characters)'    
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Passwords must match'
        if EMAIL_REGEX.match(postData['email']) == None:
			errors['email_format'] = "Email must be valid."
        if postData['date_of_birth'] == None:
            error['date_of_birth'] = 'Please enter a birthday'
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
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __repr__(self):
        return "<User object: {} {} {} {} {} >".format(self.name, self.alias, self.email, self.password, self.date_of_birth)

class QuoteManager(models.Manager):
    def item_validator(self, postData):
        quote_errors = {}
        if len(postData['quote_name']) < 3 :
            quote_errors['quote_name'] = 'Must be at least 3 characters'
        return quote_errors

class Quote (models.Model):
    quote_name = models.CharField(max_length=255)
    quote_by = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name= "quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    def __repr__(self): 
        return "<Item object: {} {} {} >".format(self.quote_name, self.quote_by, self.users)

class Favorite (models.Model):
    user = models.ForeignKey(User, related_name='favorite')
    quotes = models.ManyToManyField(Quote, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
