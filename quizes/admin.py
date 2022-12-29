from django.contrib import admin
from .models import Quiz, Region, Question, Grade

from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources, widgets

class ForeignKeyWidget(widgets.ForeignKeyWidget):
    def get_queryset(self, value, row):
        # Custom queryset filtering based on the value
        return self.model.objects.filter(name=value)

class QuizResource(resources.ModelResource):

    grade = fields.Field(
        attribute="grade",
        column_name="grade",
        widget=widgets.ForeignKeyWidget(Grade, 'grade'),
    )

    class Meta:
        model = Quiz
        fields = ('id', 'lng_title', 'subject_title', 'grade', 'number_of_questions')

class QuizAdmin(ImportExportModelAdmin):
    resource_class = QuizResource
    search_fields = ('id', 'subject_title' )
    list_display = ('id', 'subject_title','lng_title', 'grade')

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
    search_fields = ('subject_id__id', 'subject_id__subject_title', 'question')
    list_display = ('question','subject_id', 'answers')

class RegionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'region_name')

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Grade)