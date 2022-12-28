from django.db import models
from quizes.models import Quiz
from django.contrib.auth.models import User
# Create your models here.

class Result(models.Model):
    region = models.CharField(max_length=200, null=True, blank=True)
    school = models.CharField(max_length=200, null=True, blank=True)
    class_name = models.CharField(max_length=200, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Тест")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    score = models.FloatField(verbose_name="Балл")
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.quiz.subject_title) + "-" + self.user.get_full_name() + " " +  str(self.score)
    
    class Meta:
        verbose_name_plural = 'Результаты'

