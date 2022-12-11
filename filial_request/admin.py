from django.contrib import admin
from .models import RequestQuiz, AddStudent
# Register your models here.

class RequestQuizAdmin(admin.ModelAdmin):
    list_display = ('region', 'name', 'limit_start','limit_end', 'is_active')

admin.site.register(RequestQuiz, RequestQuizAdmin)
# admin.site.register(AddStudent)
