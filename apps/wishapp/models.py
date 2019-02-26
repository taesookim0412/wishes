from django.db import models
import re, bcrypt

# Create your models here.
class accountManager(models.Manager):
    def acc_validator(self, postData):
        errors = { }
        if len(postData['firstname']) < 2 or not re.match("^[A-Za-z]*$", postData['firstname']):
            errors["firstname"] = "First name must be greater than two characters and all letters."
        if len(postData['lastname']) < 2 or not re.match("^[A-Za-z]*$", postData['lastname']):
            errors["lastname"] = "Last name must be greater than two characters and all letters."
        if len(postData['email']) < 3 or not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            errors["email"] = "Email must have at least 3 characters and have an @ sign with a period trailing somewhere after."
        if account.objects.filter(email = postData['email']).exists():
            errors["emailtaken"] = "Email already exists!"
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters long."
        if postData['password'] != postData['password2']:
            errors["password2"] = "Password must match."
        return errors
    def login_validator(self, postData):
        errors = { }
        if account.objects.filter(email = postData['loginemail']).exists():
            if not bcrypt.checkpw(postData['loginpassword'].encode(), account.objects.get(email=postData['loginemail']).password.encode()):
                errors["password3"] = "Password is wrong!"
        else:
            errors["emailnotexist"] = "Email doesn't exist!"
        return errors
    def update_validator(self, postData, sessionData):
        errors = { }
        if not account.objects.get(id=sessionData['id']).email == postData['email']:
            if account.objects.filter(email = postData['email']).exists():
                errors["emailexists"] = "Email already exists!"
        if len(postData['firstname']) < 2 or not re.match("^[A-Za-z]*$", postData['firstname']):
            errors["firstname"] = "First name must be greater than two characters and all letters."
        if len(postData['lastname']) < 2 or not re.match("^[A-Za-z]*$", postData['lastname']):
            errors["lastname"] = "Last name must be greater than two characters and all letters."
        if len(postData['email']) < 3 or not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            errors["email"] = "Email must have at least 3 characters and have an @ sign with a period trailing somewhere after."
        return errors
            
        
class wishManager(models.Manager):
    def wish_validator(self, postData):
        errors = { }
        if len(postData['wish']) < 3:
            errors["wishlen"] = "Wish field must contain at least 3 characters!"
        if len(postData['desc']) < 3:
            errors["desclen"] = "Description field must contain at least 3 characters!"
        return errors

class account(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    objects = accountManager()

class grantedwish(models.Model):
    wishtitle = models.CharField(max_length=35)
    wisher = models.CharField(max_length=35)
    creater = models.ForeignKey(account, related_name="creater")
    dateadded = models.DateField()
    dategranted = models.DateField()
    likes = models.CharField(max_length=25)
    likers = models.ManyToManyField(account, related_name="liker")
    totalgranted = models.CharField(max_length=35)

class wish(models.Model):
    wishtitle = models.CharField(max_length=35)
    wishdesc = models.CharField(max_length=200)
    account = models.ForeignKey(account, related_name="wish")
    dateadded = models.DateField()
    grantedwish = models.ManyToManyField(grantedwish, related_name="wish")
    objects = wishManager()
