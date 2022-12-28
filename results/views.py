from django.shortcuts import render
from userprofile.models import Profile
from .models import Result
from django.contrib.auth.models import User
import pandas as pd
from django.http import HttpResponse
from django.views.generic import ListView
from django.db.models import Q
import datetime
import xlwt
from django.core.paginator import Paginator

# Create your views here.
def export_result_to_excel(request):
    results=Result.objects.filter(school = request.user.profile.school)
    profile = Profile.objects.all()
    data = []
    for res in results:
            data.append({
            "Регион": res.region,
            "Школа": res.school,
            "Класс": res.class_name,
            "Ф.И.О": res.user.get_full_name(),
            "ИИН": res.user,
            "Предмет": res.quiz,
            "Балов из 100": res.score,
        })
    pf = pd.DataFrame(data)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="export_results.xls"'

    pf.to_excel(response)
    return response

def export_to_excel_btn(request):
    responce = HttpResponse(content_type='application/ms-excel')
    responce['Content-Disposition'] = 'attachmet; filename=Result'+ \
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Result')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ИИН', 'Предмет1', 'Общий бал']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()

    rows = Result.objects.filter(user = request.user).values_list(
         'user__username', 'quiz__subject_title', 'score'
    )

    for row in rows:
        row_num +=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(responce)
    return responce


def superadmin(request):
    user=User.objects.all()
    profile = Profile.objects.all()
    results=Result.objects.all()

    paginator = Paginator(Result.objects.all(), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = { 'user': user, 'results': results, 'profile': profile, 'page_obj':page_obj }

    return render(request,'stats/superadmin.html', context)
    
class SearchResultsView(ListView):
    model = Result
    template_name = 'stats/search_results.html'

    def get_queryset(self): 
        query = self.request.GET.get("q")
        object_list = Result.objects.filter(
            Q(class_name__icontains=query)
        )
        return object_list

def individual(request):
    user=User.objects.all()
    results=Result.objects.filter(user = request.user)
    user = request.user
    profile = Profile.objects.get(user=user)

    context = { 'user': user, 'results': results, 'profile': profile, 'region':profile.region,
            'school':profile.school,
            'class_name':profile.class_name }
    return render(request, "login/individual.html", context)