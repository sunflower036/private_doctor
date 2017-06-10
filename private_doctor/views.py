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
            models.Doctor.objects.create(user=username, pwd=password,
                                         sex=sex, email=email)
            return HttpResponseRedirect('/doctor/')
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
    try:
        if models.Doctor.objects.filter(user=request.session['user'], 
                                        pwd=request.session['pwd']):
            return render(request, 'family.html')
        else:
            return HttpResponseRedirect('/login')
    except:
        return HttpResponseRedirect('/login')


def fail_login(request):
    return render(request, "fail_login.html")


def doctor_info(request):
    return render(request, "doctor_info.html")


def manage(request):
    return render(request, "manage.html")


def test(request):
    print(request.POST)
    data = {
        'messages': [{
            'time': 'asdas',
            'family': 'asdhjkqwhjek'
        }]
    }
    return render(request, "doctor.html", data)
