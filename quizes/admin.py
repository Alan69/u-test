from django.contrib import admin
from .models import Quiz, Region, School, Grade, Filial, UserQuizAttempt, Question, QuizLanguage

from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources, widgets


class QuizResource(resources.ModelResource):

    class Meta:
        model = Quiz

class QuizAdmin(ImportExportModelAdmin):
    resource_classes = [QuizResource]
    search_fields = ('id', 'subject_title' )
    list_display = ('id', 'subject_title','lng_title', 'grade2')

class QuestionResource(resources.ModelResource):

    quiz = fields.Field(
        attribute="subject_id",
        column_name="subject_id",
        widget=widgets.ForeignKeyWidget(Quiz),
    )

    class Meta:
        model = Question

class QuestionAdmin(ImportExportModelAdmin):
    resource_classes = [QuestionResource]
    search_fields = ('subject_id__id', 'subject_id__subject_title')
    list_display = ('question','subject_id')



admin.site.register(Quiz, QuizAdmin)
admin.site.register(Region)
# admin.site.register(School)
# admin.site.register(Grade)
# admin.site.register(Filial)
# admin.site.register(UserQuizAttempt)
# admin.site.register(QuizLanguage)
admin.site.register(Question, QuestionAdmin)