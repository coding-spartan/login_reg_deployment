from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages 
from models import *  
import bcrypt


def index(request):
    request.session.clear()
    return render(request, ('first_app/index.html'))

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hash1, date_of_birth=request.POST['date_of_birth'])       
            user = User.objects.get(email=request.POST['email'])
            request.session['id'] = user.id
            request.session['name'] = user.name
        return redirect('/quotelist')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            user = User.objects.get(email=request.POST['email'])
            request.session['id'] = user.id
            request.session['name'] = user.name
        return redirect ('/quotelist')

def quotelist(request):
    if 'name' not in request.session:
        return redirect('/')
    if len(Favorite.objects.filter(user=User.objects.get(id=request.session['id']))) == 0:
        Favorite.objects.create(user=User.objects.get(id=request.session['id']))
    context = {
        'favorite': Favorite.objects.get(user=User.objects.get(id=request.session['id'])).quotes.order_by('-created_at'),
        'other_favorite': Favorite.objects.all(),
        'user_favorite': Favorite.objects.get(user=request.session['id'])
    } 
    return render(request, 'first_app/quotelist.html', context)

def contribute(request):
    if 'name' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        quote_errors = Quote.objects.item_validator(request.POST)
        if len(quote_errors):
            for tag, error in quote_errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/quotelist')
        else:
            this_quote = Quote.objects.create(quote_name=request.POST['quote_name'], quote_by=request.POST['quote_by'], user=User.objects.get(id=request.session['id']))
            this_favorite = Favorite.objects.get(user=User.objects.get(id=request.session['id']))
            this_favorite.quotes.add(this_quote)
            return redirect('/quotelist')

def user_quotes(request, quote_id):
    if 'name' not in request.session:
        return redirect('/')
    context = {
        'quote': Quote.objects.get(id=quote_id),
        'users': Quote.objects.get(id=quote_id).favorites.all()
    }
    return render(request, 'first_app/user_quotes.html', context)

def add_quotelist(request, quote_id):
    if 'name' not in request.session:
        return redirect('/')
    add_quote = Quote.objects.get(id=quote_id)
    my_favorite = Favorite.objects.get(user=User.objects.get(id=request.session['id']))
    my_favorite.quotes.add(add_quote)
    return redirect('/quotelist')

def remove(request, quote_id):
    if 'name' not in request.session:
        return redirect('/')
    remove_quote = Favorite.objects.get(user=User.objects.get(id=request.session['id'])).quotes.get(id=quote_id)
    favorite = Favorite.objects.get(user=User.objects.get(id=request.session['id']))
    favorite.quotes.remove(remove_quote)
    return redirect('/quotelist')









