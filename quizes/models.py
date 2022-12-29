from django.db import models

class Region(models.Model):
    region_name = models.CharField(max_length=255, verbose_name="Регион")

    def __str__(self):
        return self.region_name
    
    class Meta:
        verbose_name_plural = 'Регионы'

class Grade(models.Model):
    grade = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.grade
    
    class Meta:
        verbose_name_plural = 'Классы'

SIMESTR_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4')
)

class Quiz(models.Model):
    id = models.IntegerField(primary_key=True)
    lng_title = models.CharField(max_length=200, null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    subject_title = models.CharField(max_length=200, blank=True, verbose_name='Предмет')
    number_of_questions = models.IntegerField(verbose_name="Количество вопросов", default=15, null=True, blank=True)
    time = models.IntegerField(help_text="В минутах", verbose_name="Время теста", default=45, null=True, blank=True)
    required_score_to_pass = models.IntegerField(help_text="%", verbose_name="Проходной балл ", default=50, null=True, blank=True)

    def __str__(self):
        return self.subject_title

    class Meta:
        verbose_name_plural = 'Тесты'

class Question(models.Model):
    question = models.CharField(max_length=3000, null=True, blank=True)
    image_path = models.CharField(max_length=2500, null=True, blank=True)
    var1 = models.CharField(max_length=3000, null=True, blank=True)
    var2 = models.CharField(max_length=3000, null=True, blank=True)
    var3 = models.CharField(max_length=3000, null=True, blank=True)
    var4 = models.CharField(max_length=3000, null=True, blank=True)
    var5 = models.CharField(max_length=3000, null=True, blank=True)
    answers = models.CharField(max_length=20, null=True, blank=True)
    simestr = models.IntegerField(verbose_name="Четверть", choices=SIMESTR_CHOICES, default=1, null=True, blank=True)
    subject_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name_plural = 'Вопросы'