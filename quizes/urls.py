from django.urls import path
from .views import (
    quiz,
    quiz_view,
    mainpage,
    subject,
    remove_tags,
    replace_img_path,
)

urlpatterns = [
    path('', mainpage, name='mainpage'),
    path('subject/', subject, name='subject'),
    path('quiz/<int:id>/', quiz, name='main-view'),
    path('quiz/<int:id>/<pk>/', quiz_view, name='quiz-view'),

    path('remove_tags/<int:id>/', remove_tags, name='remove_tags'),
    path('replace_img_path/<int:id>/', replace_img_path, name='replace_img_path'),
]