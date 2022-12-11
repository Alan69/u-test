from django.db import models
import random
from django.contrib.auth.models import User

class Region(models.Model):
    region_name = models.CharField(max_length=255, verbose_name="Регион")

    def __str__(self):
        return self.region_name
    
    class Meta:
        verbose_name_plural = 'Регионы'

class Filial(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    filial_name = models.CharField(max_length=255, verbose_name="Филиал")

    def __str__(self):
        return self.filial_name

    class Meta:
        verbose_name_plural = 'Филиал'

class School(models.Model):
    filial_name = models.ForeignKey(Filial, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=255, verbose_name="Школа")

    def __str__(self):
        return self.school_name
    
    class Meta:
        verbose_name_plural = 'Школы'

GRADE_CHOICES = (
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
    (11, '11'),
)

class Grade(models.Model):
    grade = models.IntegerField(choices=GRADE_CHOICES, default=4)

    def __str__(self):
        return f"{str(self.grade)}" + " Класс"
    
    class Meta:
        verbose_name_plural = 'Классы'

LANGUAGE_CHOICES = (
    (1, 'русский'),
    (2, 'казахский')
)

SIMESTR_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4')
)

class QuizLanguage(models.Model):
    lng_id = models.CharField(max_length=200, null=True, blank=True)
    lng_title = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.lng_title


class Quiz(models.Model):

    LANGUAGE_TYPES = (
    ('RU', 'RU'),
    ('KZ', 'KZ'),
     )

    id = models.IntegerField(primary_key=True)
    lng_id = models.CharField(max_length=200, null=True, blank=True)
    lng_title = models.CharField(max_length=200, null=True, blank=True)
    subject_title = models.CharField(max_length=200, blank=True, verbose_name='Предмет')
    grade2 = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    number_of_questions = models.IntegerField(verbose_name="Количество вопросов", default=15, null=True, blank=True)
    simestr = models.IntegerField(verbose_name="Четверть", choices=SIMESTR_CHOICES, default=1, null=True, blank=True)
    time = models.IntegerField(help_text="В минутах", verbose_name="Время теста", null=True, blank=True)
    required_score_to_pass = models.IntegerField(help_text="%", verbose_name="Проходной балл ", null=True, blank=True)
    # first_quiz = models.BooleanField(default=False)
    # second_quiz = models.BooleanField(default=False)
    # third_quiz = models.BooleanField(default=False)
    # fourth_quiz = models.BooleanField(default=False)
    # fifth_quiz = models.BooleanField(default=False)
    def __str__(self):
        return self.subject_title

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Тесты'

class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    level = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=2000, null=True, blank=True)
    subcategory = models.CharField(max_length=2000, null=True, blank=True)
    decision = models.CharField(max_length=2000, null=True, blank=True)
    question = models.CharField(max_length=2000, null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    var1 = models.CharField(max_length=2000, null=True, blank=True)
    var2 = models.CharField(max_length=2000, null=True, blank=True)
    var3 = models.CharField(max_length=2000, null=True, blank=True)
    var4 = models.CharField(max_length=2000, null=True, blank=True)
    var5 = models.CharField(max_length=2000, null=True, blank=True)
    answers = models.CharField(max_length=200, null=True, blank=True)
    subject_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name_plural = 'Вопросы'

class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attempt = models.DateTimeField(auto_now_add =True)