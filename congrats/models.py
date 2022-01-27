from django.db import models
from django.utils import timezone



class CustomUser(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=300, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=13)
    date_of_birth_day = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Authenticated Users'
        verbose_name_plural = 'Authenticated User'
        
