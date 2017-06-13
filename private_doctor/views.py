# coding: utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from . import models
__author__ = 'Administrator'


def login(request):
    if request.method == 'POST':
        user = request.POST.get("username", None)
        pwd = request.POST.get("password", None)
        identity = request.POST.get("identity", None)
        if identity == "doctor":
            compare_user = models.Doctor.objects.filter(user=user, pwd=pwd)
            if compare_user:
                request.session['user'] = user
                request.session['pwd'] = pwd
                return HttpResponseRedirect('/doctor/')
            else:
                return render(request, "fail_login.html")

        else:
            compare_user = models.Family.objects.filter(user=user, pwd=pwd)
            if compare_user:
                request.session['user'] = user
                request.session['pwd'] = pwd
                return HttpResponseRedirect('/family/')
            else:
                return render(request, "fail_login.html")
    else:
            return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        sex = request.POST.get("sex", None)
        email = request.POST.get("email", None)
        identity = request.POST.get("identity", None)
        if identity == "doctor":
            try:
                models.Doctor.objects.create(user=username, pwd=password,
                                             sex=sex, email=email)
                return HttpResponseRedirect('/doctor/')
            except:
                return render(request, "name_error.html")
        else:
            try:
                models.Family.objects.create(user=username, pwd=password,
                                             sex=sex, email=email)
                return HttpResponseRedirect('/family/')
            except:
                return render(request, "name_error.html")

    else:
        return render(request, 'register.html')

# def user(request):
#     if request.method=="POST":
#         username=request.POST.get("username", None)
#         password=request.POST.get("password", None)
#         sex=request.POST.get("sex", None)
#         email=request.POST.get("email", None)
#         models.UserInfo.objects.create(user=username,pwd=password,sex=sex,email=email)
#     userlist=models.UserInfo.objects.all()
#     return render(request, "user.html",{"data":userlist})


def doctor(request):
    try:
        if models.Doctor.objects.filter(user=request.session['user'],
                                        pwd=request.session['pwd']):

            df = models.Appointment.objects.filter(doctor__user=request.session['user']).all()
            families = []
            for record in df:
                family = get_family(record.family.user,families)
                if family is not False:
                    family.times.append(record.time)
                else:
                    families.append({'user': record.family.user,
                                     'times': [record.time]})

            data = {
                "families": families
            }
            return render(request, 'doctor.html', data)
        else:
            return HttpResponseRedirect('/login')
    except:
        return HttpResponseRedirect('/login')


def get_family(user, families):
    for family in families:
        if family.user == user:
            return family
    return False


def family(request):
    if models.Family.objects.filter(user=request.session['user'],
                                   pwd=request.session['pwd']):
        family = models.Family.objects.filter(user=request.session['user'])
        df = models.Family_Doctor.objects.filter(family__user=request.session['user'])
        if len(df) == 0:
            return HttpResponseRedirect('/choice/')
        else:
            doctor =  models.Family_Doctor.objects.filter(family__user=request.session['user'])[0]
            advice = family[0].advice
            return render(request, 'family.html',{"doctor":doctor.doctor_name,"advice":advice})
            #return render(request, 'family.html')
    else:
       return HttpResponseRedirect('/login')


def fail_login(request):
    return render(request, "fail_login.html")


def doctor_info(request):
    if models.Doctor.objects.filter(user=request.session['user'],
                                    pwd=request.session['pwd']):
        doctor = models.Doctor.objects.filter(user=request.session['user'])[0]
        if request.method == "POST":
            text = request.POST.get("desc", None)
            doctor.text=text
            doctor.save()
        desc = doctor.text
        return render(request, "doctor_info.html", {"desc": desc})
    else:
        return HttpResponseRedirect('/login')


def manage(request):
    if models.Doctor.objects.filter(user=request.session['user'],
                                    pwd=request.session['pwd']):  # 检测登录
        doctor = models.Doctor.objects.filter(user=request.session['user'])[0]
        fds = models.Family_Doctor.objects.filter(doctor=doctor).all()
        return render(request, "doctor_info.html", {"fds": fds})
    else:
        return HttpResponseRedirect('/login')


def test(request):
    print(request.POST)
    data = {
        'messages': [{
            'time': 'asdas',
            'family': 'asdhjkqwhjek'
        }]
    }
    return render(request, "doctor.html", data)

def choice(request):
    if models.Family.objects.filter(user=request.session['user'],
                                        pwd=request.session['pwd']):
        doctors=models.Doctor.objects.all()
        if request.method=="POST":
            user = request.POST.get("user",None)
            doctor = models.Doctor.objects.filter(user = user)[0]
            family = models.Family.objects.filter(user = request.session['user'])[0]
            models.Family_Doctor.objects.create(doctor_name=doctor.user,family=family)
            return HttpResponseRedirect('/family/')
        return render(request,"choice.html",{"doctors":doctors})
    else:
        return HttpResponseRedirect('/login/')

def appointment(request):
    return render(request,"appointment.html")

def history(request):
    if models.Family.objects.filter(user=request.session['user'],
                                    pwd=request.session['pwd']):
        family = models.Family.objects.filter(user=request.session['user'])[0]
        if request.method == "POST":
            text = request.POST.get("desc", None)
            family.text=text
            family.save()
        desc = family.text
        return render(request, "history.html", {"desc": desc})
    else:
        return HttpResponseRedirect('/login')