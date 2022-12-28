from django.urls import path
from .views import request_page, add_students

urlpatterns = [
    path('', request_page, name='request_page'),
    path('addstudent/', add_students, name="addstudent"),
]