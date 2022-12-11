from django.db import models
from django.contrib.auth.models import User
from quizes.models import Region
from django.db.models.signals import post_save
from django.dispatch import receiver
from results.models import Result
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    school = models.CharField(max_length=255, blank=True, null=True)
    class_name = models.CharField(max_length=255, blank=True)
    is_teacher = models.BooleanField(default=False)
    is_filial = models.BooleanField(default=False)
    # results = models.ManyToManyField(Result)

    def __str__(self):
        return str(self.user)
 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Teacher(models.Model):
    teacher_user = models.OneToOneField(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name="%(app_label)s_%(class)s_related")

    def __str__(self):
        return str(self.teacher_user)