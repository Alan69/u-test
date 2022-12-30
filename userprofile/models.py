from django.db import models
from quizes.models import Region
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город")
    school = models.CharField(max_length=255, null=True, blank=True, verbose_name="Школа") 
    class_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Класс") 
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username
