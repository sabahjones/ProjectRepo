from django.shortcuts import render, redirect
import re
from django.contrib import messages
import bcrypt
import datetime
from datetime import timedelta

from .models import *

def index(request):
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    print "date now = ", today
    print "same time tomorrow is ", tomorrow
    return render(request, 'firstapp/index.html')


def appointments(request):
    user = Users.objects.filter(email=request.session['email'])
    for u in user:
        id = user
    #appointments = Appointments.objects.filter(user_id=u.id).order_by('time')
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    todayappt = Appointments.objects.filter(user_id=u.id).filter(time__range=[today, tomorrow]).order_by('time')
    tomappt = Appointments.objects.filter(user_id=u.id).exclude(time__range=[today, tomorrow]).order_by('time')

    context = {"user": user, 'appointments': appointments, 'todayappt': todayappt, 'tomappt': tomappt}

    return render(request, 'firstapp/appointments.html', context)


def register(request):
    if request.method == "POST":
        errors = "false"
        result = re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', request.POST['email'])
        if len(request.POST['name']) < 2:
            messages.error(request, 'your name must be longer than 2 characters')
            errors = "true"
        if result == None:
            messages.error(request, 'that email is invalid')
            errors = "true"
        if len(request.POST['password']) < 8:
            messages.error(request, 'password must be longer than 8 characters')
            errors = "true"
        if request.POST['password'] != request.POST['password2']:
            messages.error(request, 'passwords do not match')
            errors = "true"
        if len(request.POST['birthday']) < 4:
            messages.error(request, 'Please enter a value for birthday')
            errors = "true"
        if errors == "true":
            return redirect('/')
        if errors == "false":
            hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            Users.objects.create(name=request.POST['name'], email=request.POST['email'], password=hashpw, birthday=request.POST['birthday'])
            print ".....new user just created......"
            request.session['name'] = request.POST['name']
            request.session['email'] = request.POST['email']
            print "....sessions storing user name and email (from from data)"

    return redirect('/appointments')


def login(request):
    if request.method == "POST":
        user = Users.objects.filter(email=request.POST['email'])
        if user.count() == 0:
            messages.error(request, 'email not in database, please register')
            return redirect ('/')
        for info in user:
            if bcrypt.checkpw(request.POST["password"].encode(), info.password.encode()):
                request.session['name'] = info.name
                request.session['email'] = info.email
                print info.name
                return redirect('/appointments')
            else:
                messages.error(request, 'your password is incorrect, please try again')
    return redirect ('/')


def makeapp(request, id):
    if request.method == "POST":
        errors = "false"
        datetimevar = request.POST['date'] + str(" ") + str(request.POST['time'])
        print "concat date and time value is ", datetimevar
        today = datetime.now()
        if len(request.POST['task']) < 1:
            messages.error(request, "please enter a name for your appointment in task")
            errors = "true"
        if str(today) > datetimevar:
            print "You entered an invalid date/time, please re-enter."
            messages.error(request, 'Please enter a valid appointment date/time')
            errors = "true"
        if len(request.POST['time']) < 5:
            messages.error(request, 'please enter a valid time for your appointment')
            errors = "true"
        if errors == "true":
            return redirect('/appointments')
        else:
            print "that is a valid date and time you entered!"
            Appointments.objects.create(task=request.POST['task'], time=datetimevar, status="Pending", user_id=id)

    return redirect('/appointments')


def edit(request, id):
    edit = Appointments.objects.filter(id=id)
    context = {'edit': edit}
    return render(request, 'firstapp/edit.html', context)


def update(request, id):
    if request.method =="POST":
        newtime = request.POST['date'] + str(" ") + str(request.POST['time'])
        print "new time is ", newtime
        print "passed id =", id
        print request.POST['task'], request.POST['status']
        Appointments.objects.filter(id=id).update(task=request.POST['task'], status=request.POST['status'], time = newtime)
    return redirect('/appointments')


def delete(request, id):
    Appointments.objects.filter(id=id).delete()
    return redirect ('/appointments')


def logoff(request):
    request.session.clear()
    return redirect('/')