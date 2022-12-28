from django.urls import path
from .views import (
    quiz,
    quiz_view,
    mainpage,
    subject,
    remove_tags,
)

urlpatterns = [
    path('', mainpage, name='mainpage'),
    path('subject/', subject, name='subject'),
    path('quiz/<int:id>/', quiz, name='main-view'),
    path('quiz/<int:id>/<pk>/', quiz_view, name='quiz-view'),

    path('remove_tags/<int:id>/', remove_tags, name='remove_tags'),
]