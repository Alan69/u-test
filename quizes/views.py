from django.shortcuts import render
# from userprofile.models import Profile
from .models import Quiz, Question, Grade
from results.models import Result
# from django.contrib.auth.models import User
from userprofile.models import User
import math
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import random
from .cleanTags import cleanhtml, removepath

def remove_tags(request, id):
    obj = Question.objects.filter(subject_id = id)
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
    return HttpResponse("Успешно удалено")

def replace_img_path(request, id):
    obj = Question.objects.filter(subject_id = id)
    for q in obj:
        img = removepath(q.image_path)
        q.image_path = img
        q.save(update_fields=["image_path"])
    return HttpResponse("Успешно изменино")

@login_required(login_url='/login/')
def mainpage(request):
    model=User.objects.all()
    results=Result.objects.filter(user = request.user)
    context = { 'user': model, 'results': results}
    return render(request,'quizes/mainpage.html', context)

def subject(request):
    user_class_name = request.user.class_name
    user_class_name = ''.join(filter(str.isdigit, user_class_name))

    if request.user.is_staff:
        grade = Grade.objects.all()
    else:
        grade = Grade.objects.filter(grade = user_class_name)
    context = {'grade':grade}
    return render(request,'quizes/subject.html', context)

def quiz(request, id):
    grade = Grade.objects.get(pk=id)
    quiz = Quiz.objects.filter(grade = grade)
    context = {'quiz': quiz, 'grade': grade}
    return render(request, 'quizes/main.html', context)

def quiz_view(request, id, pk):
    if request.method == 'POST':
        # print(request.POST)
        quiz = Quiz.objects.get(id=pk)
        questions=Question.objects.filter(subject_id=pk)[0:15]
        
        score=0
        wrong=0
        correct=0
        total=0

        for q in questions:
            total+=1
            answer = request.POST.get(q.question) # Gets user’s choice, i.e the key of answer
            # print("вопрос: " + str(q.answers) + " id: " +str(q.id))
            # print("ответ: " + str(answer))

            if q.answers == answer:
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = math.trunc(score)/(total*10) *100

        user = request.user
        # profile = Profile.objects.get(user=user)
        
        context = {
            'score':math.trunc(score),
            'time': request.POST.get('timer'), 
            'correct':correct,
            'wrong':wrong,
            'percent':math.trunc(percent),
            'total':total,
            'region':user.region,
            'school':user.school,
            'class_name':user.class_name
        }

        Result.objects.create(region=user.region, school=user.school, class_name=user.class_name, quiz=quiz, user=user, score = math.trunc(percent))
        return render(request,'quizes/result.html', context)
    else:
        quiz = Quiz.objects.get(id=pk)

        if request.user.is_staff:
            questions_numbers = 180
        else:
            questions_numbers = 15
        
        questions = sorted(Question.objects.filter(subject_id=quiz)[0:questions_numbers], key=lambda x: random.random())

        context = {
            'questions': questions,
            'quiz': quiz
        }
        return render(request,'quizes/quiz.html', context)