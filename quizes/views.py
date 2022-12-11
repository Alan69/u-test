from encodings import utf_8
import uuid
from django.shortcuts import render, redirect
from userprofile.models import Profile, Teacher
from .models import Quiz, Question, Grade
from django.http import JsonResponse
from results.models import Result
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate
from django.contrib.auth import login as auth_login
import math
from .forms import *
import pandas as pd
from django.contrib.auth.decorators import login_required
import os
from django.http import HttpResponse
import random
from .cleanTags import cleanhtml
from django.views.generic import ListView
from django.db.models import Q
import datetime
import xlwt
from django.core.paginator import Paginator

def remove_tags(request):
    obj = Question.objects.all()
    for q in obj:
        t = cleanhtml(q.question)
        var1 = cleanhtml(q.var1)
        var2 = cleanhtml(q.var2)
        var3 = cleanhtml(q.var3)
        var4 = cleanhtml(q.var4)
        var5 = cleanhtml(q.var5)
        q.question = t
        q.var1 = var1
        q.var2 = var2
        q.var3 = var3
        q.var4 = var4
        q.var5 = var5
        q.save(update_fields=["question"])
        q.save(update_fields=["var1"])
        q.save(update_fields=["var2"])
        q.save(update_fields=["var3"])
        q.save(update_fields=["var4"])
        q.save(update_fields=["var5"])
    return HttpResponse(t)

def export_result_to_excel(request):
    results=Result.objects.filter(school = request.user.profile.school)
    profile = Profile.objects.all()
    # for p in profile:
    #     for r in results:
    #         if r.user == p.user:
    #             if r.quiz.first_quiz == True:
    #                 quiz1 = r.quiz
    #             elif r.quiz.second_quiz == True:
    #                 quiz2 = r.quiz
    #             elif r.quiz.third_quiz == True:
    #                 quiz3 = r.quiz
    #             elif r.quiz.fourth_quiz == True:
    #                 quiz4 = r.quiz
    #             elif r.quiz.fifth_quiz == True:
    #                 quiz5 = r.quiz

    data = []
    for res in results:
        # if res.school == request.user.profile.school:
            data.append({
            "Регион": res.region,
            "Школа": res.school,
            "Класс": res.class_name,
            "Ф.И.О": res.user.get_full_name(),
            "ИИН": res.user,
            "Предмет": res.quiz,
            # "Предмет2": quiz2,
            # "Предмет3": quiz3,
            # "Предмет4": quiz4,
            # "Предмет5": quiz5,
            "Балов из 100": res.score,
            # "Средний бал": res.score
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

@login_required(login_url='/login/')
def mainpage(request):
    model=User.objects.all()
    results=Result.objects.filter(user = request.user)
    context = { 'user': model, 'results': results}
    return render(request,'quizes/mainpage.html', context)

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

def subject(request):
    quiz = Quiz.objects.all()
    grade = Grade.objects.all()
    context = {'quiz': quiz, 'grade':grade}
    return render(request,'quizes/subject.html', context)

def quiz(request, id):
    grade = Grade.objects.get(pk=id)
    quiz = Quiz.objects.filter(grade2 = grade)
    context = {'quiz': quiz, 'grade': grade}
    return render(request, 'quizes/main.html', context)

# def quiz_view(request, pk):
#     quiz = Quiz.objects.get(pk=pk)
#     question = Question.objects.filter(subject_id=quiz).order_by('?')[0:quiz.number_of_questions]
#     return render(request, 'quizes/quiz.html', {'questions': question})

def quiz_view(request, id, pk):
    if request.method == 'POST':
        print(request.POST)
        quiz = Quiz.objects.get(id=pk)
        questions=Question.objects.filter(subject_id=pk)[0:180]

        score=0
        wrong=0
        correct=0
        total=0

        for q in questions:
            total+=1
            # print(q.answers)
            # print(request.POST.get(q.question))
            # if q.answers == request.POST.get(q.question):
            a = random.randint(1,8)
            if a % 2 == 0:
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = math.trunc(score)/(total*10) *100

        user = request.user
        profile = Profile.objects.get(user=user)
        
        context = {
            'score':math.trunc(score),
            'time': request.POST.get('timer'), 
            'correct':correct,
            'wrong':wrong,
            'percent':math.trunc(percent),
            'total':total,
            'region':profile.region,
            'school':profile.school,
            'class_name':profile.class_name
        }

        Result.objects.create(region=profile.region, school=profile.school, class_name=profile.class_name, quiz=quiz, user=user, score = math.trunc(percent))
        return render(request,'quizes/result.html', context)
    else:
        quiz = Quiz.objects.get(id=pk)
        # LastTenR = sorted(Question.objects.filter(subject_id=quiz)[0:quiz.number_of_questions], key=lambda x: random.shuffle(x))
        LastTenR = Question.objects.filter(subject_id=pk).order_by('?')[0:180]
        context = {
            'questions': LastTenR,
            'quiz': quiz
        }
        return render(request,'quizes/quiz.html', context)

def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    question = Question.objects.filter(subject_id=quiz)
    questions = []
    for q in question:
        answers = []
        for a in q.var1 and q.var2 and q.var3 and q.var4 and q.var5:
            answers.append(a)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def save_quiz_view(request, pk):
    if is_ajax(request=request):
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(question=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        # filial = Filial.objects.get(pk=pk)
        # school = School.objects.get(pk=pk)

        score = 0
        multiplier = 100 / 15
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Question.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})
            
        score_ = score * multiplier
        # Result.objects.create(region=region, filial=filial, school=school, quiz=quiz, user=user, score = math.trunc(score_))
        
        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': math.trunc(score_), 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': math.trunc(score_), 'results': results})

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('login') 
    else: 
        form = CustomUserCreationForm()
        if request.method=='POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid() :
                user=form.save()
                return redirect('login')
        context={
            'form':form,
        }
        return render(request,'login/auth.html',context)
 
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('mainpage')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
       context={}
       return render(request,'login/login.html',context)
 
def logoutPage(request):
    logout(request)
    return redirect('login')

def individual(request):
    user=User.objects.all()
    results=Result.objects.filter(user = request.user)
    user = request.user
    profile = Profile.objects.get(user=user)

    context = { 'user': user, 'results': results, 'profile': profile, 'region':profile.region,
            'school':profile.school,
            'class_name':profile.class_name }
    return render(request, "login/individual.html", context)