from django.contrib.auth.models import AbstractUser
from django.db import models
import pytz

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(
        'email address',
        unique=True,  
        blank=False,  
        null=False,   
        error_messages={
            'unique': "Пользователь с таким email уже существует"
        }
    )
    timezone = models.CharField(
        max_length=100,
        choices=[(tz, tz) for tz in pytz.common_timezones],
        default='UTC'
    )
    receive_notifications = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'      
    EMAIL_FIELD = 'email'         
    REQUIRED_FIELDS = ['username']  

    def __str__(self):
        return f"{self.username} ({self.timezone})"