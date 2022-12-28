from django.urls import path
from .views import (
    superadmin,
    export_result_to_excel,
    SearchResultsView,
    individual,
    export_to_excel_btn
)

urlpatterns = [
    path('export_result_to_excel', export_result_to_excel, name='export_result_to_excel'),
    path('export_to_excel_btn/', export_to_excel_btn, name='export_to_excel_btn'),
    path('', superadmin, name='superadmin'),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path('individual/', individual, name='individual'),
]