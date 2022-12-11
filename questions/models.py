from django.db import models
from quizes.models import Quiz

DIFF_CHOICES = (
    ('легкий', 'легкий'),
    ('средний', 'средний'),
    ('сложный', 'сложный'),
)

SIMESTR_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
)

class AdminTest(models.Model):
    level = models.CharField(max_length=200, null=True, blank=True, verbose_name="Уровень")
    category = models.CharField(max_length=200, null=True, blank=True, verbose_name="Категория")
    subcategory = models.CharField(max_length=200, null=True, blank=True, verbose_name="Раздел")
    decision = models.CharField(max_length=200, null=True, blank=True, verbose_name="Подраздел")
    image_path = models.CharField(max_length=200, null=True, blank=True, verbose_name="Изображение")
    audio_path = models.CharField(max_length=200, null=True, blank=True, verbose_name="Аудио")
    question = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вопрос")
    var1 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 1")
    var2 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 2")
    var3 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 3")
    var4 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 4")
    var5 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 5")
    var6 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 6")
    var7 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 7")
    var8 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 8")
    var9 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 9")
    var10 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 10")
    var11 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 11")
    var12 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Вариант 12")
    answers = models.CharField(max_length=200, null=True, blank=True, verbose_name="Правильный вариант")
    group_text = models.CharField(max_length=200, null=True, blank=True, verbose_name="Групп текст")
    group_image_path = models.CharField(max_length=200, null=True, blank=True, verbose_name="Групп изображение")
    group_audio_path = models.CharField(max_length=200, null=True, blank=True, verbose_name="Групп аудио")
    lng_id = models.CharField(max_length=200, null=True, blank=True)
    lng_title = models.CharField(max_length=200, null=True, blank=True)
    subject_title = models.CharField(max_length=200, null=True, blank=True)
    grade = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name="Админ тест"
        verbose_name_plural = 'Админ тесты'

class Answer(models.Model):
    text = models.CharField(max_length=200, verbose_name="текст")
    correct = models.BooleanField(default=False, verbose_name="правильный")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="вопрос")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Вопрос: {self.question.text}, Ответ: {self.text}, Правильный: {self.correct}"
    
    class Meta:
        verbose_name="Ответ"
        verbose_name_plural = 'Ответы'



