from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from quizes.models import Region
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password, first_name, last_name, **extra_fields):
        if not username:
            raise ValueError("Необходимо указать логин")
        if not password:
            raise ValueError("Необходимо ввести пароль")
        
        user = self.model(
            username = (username),
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, first_name, last_name, **extra_fields)
    
    def create_superuser(self, username, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password, first_name, last_name, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, unique=True, max_length=254, verbose_name="username")
    first_name = models.CharField(max_length=250, verbose_name="Имя")
    last_name = models.CharField(max_length=250, verbose_name="Фамилия")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город")
    school = models.CharField(max_length=255, null=True, blank=True) 
    class_name = models.CharField(max_length=255, null=True, blank=True) 

    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"

