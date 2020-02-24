from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from wallapp.models import *
import bcrypt

# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect('/wall')
    return render(request, 'index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(first=request.POST['first'], last=request.POST['last'], email=request.POST['email'],password=pw_hash, birthday=request.POST['birthday'])
    request.session['user']=user.id
    return redirect('/wall')
    

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user=user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user']=user[0].id
            return redirect('/wall')
        return HttpResponse('Incorrect Password')
    return HttpResponse('Email not registered')

def wall(request):
    if 'user' not in request.session:
        return HttpResponse("Please Log In")
    context={
        'user': User.objects.get(id=request.session['user']),
        'messages': Message.objects.all(),
    }
    return render(request, 'wall.html', context)

def logout(request):
    del request.session['user']
    return redirect('/')

def message(request):
    user = User.objects.get(id=request.session['user'])
    Message.objects.create(user=user, message = request.POST['message'])
    return redirect('/wall')

def comment(request):
    user = User.objects.get(id=request.session['user'])
    message= Message.objects.get(id=request.POST['messageid'])
    Comment.objects.create(user=user, message=message, comment=request.POST['comment'])
    return redirect('/wall')

def delete(request, id):
    owner = Message.objects.get(id=id).user.id
    user = User.objects.get(id=request.session['user'])
    if user.id==owner:
        message = Message.objects.get(id=id)
        message.delete()
        return redirect('/wall')
    return HttpResponse('Unauthorized request')
