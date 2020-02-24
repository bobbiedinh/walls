import re
from django.db import models
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postDATA):
        errors={}
        currentDate = datetime.now().date()
        if len(postDATA['first'])<2:
            errors['first']="First Name must be 2 or more characters"
        if len(postDATA['first'])<2:
            errors['last']="Last Name must be 2 or more characters"
        EMAIL_CHECK = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_CHECK.match(postDATA['email']):
            errors['email']="Incorrect email format (john@yahoo.com)"
        elif User.objects.filter(email=postDATA['email']):
            errors['email']='Email already used'
        if len(postDATA['password'])<8:
            errors['password']="Password length must be 8 or more characters"
        elif postDATA['password']!=postDATA['confirm']:
            errors['password']="Passwords do not match"
        if len(postDATA['birthday'])<1:
            errors['birthday']='Birthday field empty'
        elif currentDate.year-datetime.strptime(postDATA['birthday'], '%Y-%m-%d').date().year<13:
            errors['birthday']="Must be 13+"
        return errors

class User(models.Model):
    first = models.CharField(max_length=45)
    last = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    birthday = models.DateField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)