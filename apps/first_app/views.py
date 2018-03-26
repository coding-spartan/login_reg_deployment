from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages 
from models import *  
import bcrypt


def index(request):
    request.session.clear()
    return render(request, ('first_app/index.html'))


def process(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            request.session['name'] = request.POST['first_name']
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash1)       
            u = User.objects.get(email=request.POST['email'])
            request.session['id'] = u.id
            return redirect('/success')


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            u = User.objects.get(email=request.POST['email'])
            request.session['id'] = u.id
            request.session['name'] = u.first_name
            return redirect ('/success')
            
            
def success(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        return render(request, ('first_app/success.html'))


