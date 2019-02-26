from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt, datetime
from apps.wishapp.models import *

# Create your views here.
def index(request):
    return render(request, "wishapp/index.html")

def register(request):
    errors = account.objects.acc_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    else:
        a = account()
        a.first_name = request.POST['firstname']
        a.last_name = request.POST['lastname']
        a.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        a.email = request.POST['email']
        a.save()
        request.session['id'] = a.id
        request.session['firstname'] = a.first_name
        return redirect('/wishes')

def login(request):
        errors = account.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            a = account.objects.get(email=request.POST['loginemail'])
            request.session['id'] = a.id
            request.session['firstname'] = a.first_name
            return redirect('/wishes')

def wishes(request):
    context = { "wishes" : wish.objects.filter(account_id=request.session['id']).values(),
    "grantedwishes" : grantedwish.objects.all(), }
    return render(request, 'wishapp/wishes.html', context)

def new(request):
    return render(request, 'wishapp/new.html')

def addwish(request):
    errors = wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/wishes/new')
    else:
        wish.objects.create(wishtitle=request.POST['wish'], wishdesc=request.POST['desc'], account=account.objects.get(id=request.session['id']), dateadded=datetime.datetime.now().date())
        return redirect('/wishes')

def addgrant(request):
    a = wish.objects.get(id=request.POST['wishid'])
    b = grantedwish.objects.create(wishtitle=a.wishtitle, wisher=a.account.first_name, dateadded=a.dateadded, dategranted=datetime.datetime.now().date(), likes=0, creater=account.objects.get(id=request.session['id']))
    a.grantedwish.add(b)
    a.delete()
    return redirect('/wishes')

def logout(request):
        if request.session['id']:
                del request.session['id']
                del request.session['firstname']
                return redirect('/')
        return redirect('/')

def remove(request):
    wish.objects.get(id=request.POST['wishid']).delete()
    return redirect('/wishes')

def edit(request, id):
    context = { "wish" : wish.objects.get(id=id) }
    return render(request, 'wishapp/edit.html', context)

def update(request):
        errors = wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/wishes/edit/' + request.POST['wishid'])
        else:
            w = wish.objects.get(id=request.POST['wishid'])
            w.wishtitle = request.POST['wish']
            w.wishdesc = request.POST['desc']
            w.save()
            return redirect('/wishes/edit/' + request.POST['wishid'])

def addlike(request):
    b = grantedwish.objects.get(id=request.POST['grantid'])
    if b.likers.filter(id=request.session['id']).count() > 0 or b.creater.id==request.session['id']:
        return redirect("/wishes")
    else:
        likecounter = grantedwish.objects.get(id=request.POST['grantid']).likes
        likecounter = int(likecounter) + 1
        b.likes = likecounter
        b.save()
        b.likers.add(account.objects.get(id=request.session['id']))
        return redirect('/wishes')

def stats(request):
        if not grantedwish.objects.last():
                return redirect('/wishes')
        else:
                grantedwishme = account.objects.get(id=request.session['id']).creater.all().values()
                granted = 0
                for times in grantedwishme:
                        granted = granted + 1
                grantedtotal = grantedwish.objects.last().id
                grantedpending = grantedtotal - granted
                context = { "grantedwishme" : account.objects.get(id=request.session['id']).creater.all().values() ,
                "granted": granted,
                "grantedtotal" : grantedtotal,
                "grantedpending" : grantedpending }
                return render(request, "wishapp/stats.html", context)