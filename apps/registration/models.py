from __future__ import unicode_literals
from django.db import models
import bcrypt 
#import datetime module
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
#format regex 
import re 
LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class UserManager(models.Manager):
    def reg_val(self, postData):
        errors = {}
        #first_name <2 and letters
        if len(postData["name"]) < 2:
            errors['name']= "Name must be atleast 2 characters long"
        if bool(re.search(r'\d', postData["name"])):
            errors['name']= "Name must be letters only"
        
        #last name <2 and letters
        if len(postData["alias"])<2:
            errors['alias'] = "Alias must be atleast 2 characters long"
        if bool(re.search(r'\d', postData["alias"])):
            errors['alias'] = "Alias must be letters only"
        
        #birthdate in past validation
        try:
            if datetime.strptime(postData["birthdate"],"%Y-%m-%d") > datetime.today(): #bonus 
                errors['birthdate'] = "Birthdate can not be in the future"
            if datetime.strptime(postData["birthdate"], "%Y-%m-%d") == False:
                errors['birthdate'] = "Birthdate can not be left blank"
        except ValueError:
            errors['birthdate'] = "Birthdate not valid"
        
        #email length and format errors 
        if len(postData["email"]) < 1:
            errors['email'] = "Email must not be blank!"
        if not EMAIL_REGEX.match(postData["email"]):
            errors['email'] = "Invalid email!"
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists"
        
        #password <1 or <8 errors 
        if len(postData["password"]) < 1:
            errors['password'] = "Password must not be blank!"
        if len(postData["password"]) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        
        #pw confirmation
        if postData["password"]!=postData["confirm_password"]:
            errors['password'] = "Password does not match confirmation"
        
        return errors #returns any errors acumulated 
    #login with password hash check via bcrypt 
       

    def login_val(self, postData):
        errors = {}  
        user = User.objects.filter(email=postData["email"])
        if len(postData["email"]) < 1:
            errors["email"] = "Please enter an email"
        if len(postData["password"])<1:
            errors["password"] = "Please enter a password"
        if not user:
            errors["email"] = "Incorrect login"
        #if password-entered hash doesn't match the database hash
        elif not bcrypt.checkpw(postData["password"].encode(), user[0].password.encode()):
            errors["email"] = "Incorrect login"
        return errors 

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length= 255)
    birthdate = models.DateTimeField(null=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
   

class UserManager(models.Manager):
    def quote_val(self, postData):
        errors = []
        #quoted by <3 and chars
        if len(postData["quoted_by"]) < 3:
            errors.append("field must be atleast 3 characters long")
        if bool(re.search(r'\d', postData["quoted_by"])):
            errors.append("Name must be letters only")
        #last name <2 and letters
        if len(postData["message"])<10:
            errors.append("Quote/message must be atleast 10 characters long")    
        if bool(re.search(r'\d', postData["message"])):
            errors.append("Quote/message must be letters only")

class Quote(models.Model):
    quote_by = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="poster", blank=True, null=True)
    faved_by = models.ManyToManyField(User, related_name="favquotes") #manytomany for the likes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





