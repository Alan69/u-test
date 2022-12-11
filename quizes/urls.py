from django.urls import path
from .views import (
    quiz,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
    mainpage,
    loginPage,
    registerPage,
    logoutPage,
    superadmin,
    export_result_to_excel,
    subject,
    remove_tags,
    SearchResultsView,
    individual,
    export_to_excel_btn
)

from filial_request.views import request_page, add_students

urlpatterns = [
    path('mainpage/', mainpage, name='mainpage'),
    path('export_result_to_excel', export_result_to_excel, name='export_result_to_excel'),
    path('export_to_excel_btn/', export_to_excel_btn, name='export_to_excel_btn'),

    path('request_page/', request_page, name='request_page'),
    path('addstudent/', add_students, name="addstudent"),

    path('subject/', subject, name='subject'),
    path('quiz/<int:id>/', quiz, name='main-view'),
    path('quiz/<int:id>/<pk>/', quiz_view, name='quiz-view'),

    path('quiz/<int:id>/<pk>/save/', save_quiz_view, name='save-view'),
    path('quiz/<int:id>/<pk>/data/', quiz_data_view, name='quiz-data-view'),
    
    path('', loginPage, name='login'),
    path('auth/', registerPage, name='auth'),
    path('logoutPage/', logoutPage, name='logoutPage'),

    path('superadmin/', superadmin, name='superadmin'),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path('individual/', individual, name='individual'),

    path('remove_tags/<int:id>/', remove_tags, name='remove_tags'),
]