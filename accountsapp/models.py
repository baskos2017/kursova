from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from magaz.settings import EMAIL_HOST_USER

# Create your models here.

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    phone_number = models.CharField(max_length=255)

class Comment(models.Model):
    text = models.CharField(max_length=255)
    id_anonymous_user = models.CharField(max_length=255)
    
    
class RegistrationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=10)

class MailMessage(models.Model):
    users = models.ManyToManyField(User)
    message = models.TextField()

    def save(self, *args, **kwargs):

       
        
        super().save(*args, **kwargs)
