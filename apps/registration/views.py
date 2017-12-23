from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
from models import *
import bcrypt

#=======================================================================================
#                       login-registration
#=======================================================================================
def index(request):
    return render(request, "beltrevapp/index.html")

def registration(request):
    errors = User.objects.reg_val(request.POST)
    if errors:
        for key, error in errors.items():
            messages.error(request, error, extra_tags="reg {}".format(key))
        return redirect('/')
    else:
        user = User.objects.create(name=request.POST["name"], alias=request.POST["alias"], birthdate=datetime.strptime(request.POST["birthdate"], "%Y-%m-%d"), email=request.POST["email"], password=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()))
        request.session['id'] = user.id
        return redirect('/success')

def login(request):
    errors = User.objects.login_val(request.POST)
    if errors:
        for key, error in errors.items():
            messages.error(request, error, extra_tags="log {}".format(key))
        return redirect("/")
    else:
        request.session["id"]=User.objects.get(email=request.POST['email']).id
        messages.success(request, "Welcome!")
        return redirect("/success")
    return errors
#=======================================================================================
#                                   Main Page 
#=======================================================================================
def success(request):
    #unpack the query for the given user based on id and first_name
    try:
        request.session['id']
    except KeyError:
        return redirect('/')

#general quotes
    user_logged = User.objects.get(id = request.session["id"])
    quotes = Quote.objects.exclude(faved_by = user_logged)

    
    context = {
        "user_logged": user_logged,
        "notfavquotes": quotes,
    }
    return render(request,"registration/success.html", context)

def unfav(request, id):
    user_logged = User.objects.get(id = request.session["id"])
    unquote = Quote.objects.get(id = id)
    unquote.faved_by.remove(user_logged)

    return redirect("/success")

def addfav(request, id):
    user_logged = User.objects.get(id = request.session["id"])
    quote = Quote.objects.get(id = id) #id from url and quote 
    quote.faved_by.add(user_logged) #connects the quote to the user that added it to faves 
    quote.save()
    return redirect("/success")

    # view all quotes by user:
def favorites(request):
    context = {
        "favquotes": User.objects.all()
        }
    # user id request for favquotes 
    return render(request, "registration/success.html", context)

def remove(request): #remove from myfav but not quote db 
    id = request.POST['id']
    quote = Quote.objects.get(id = id).delete()
    return redirect('/')

#======================================================================================
#       Create a new quote 
#======================================================================================
def create(request):
    user_logged = User.objects.get(id = request.session["id"])
    new_quote = Quote.objects.create(quote_by = request.POST['quoted_by'], message = request.POST['message'], posted_by = user_logged)
    return redirect('/success')

#=========================================================
    # page of any given poster
#=========================================================
def pages(request, id):
    poster = User.objects.get(id=id)
    quotes = Quote.objects.filter(posted_by=poster)
    count = len(quotes)

    context = {
        "poster": poster,
        "quotes": quotes,
        "count": count
    }
    return render (request, "registration/pages.html", context)
    #include: user, count, author and quote 


#=======================================================================================
#                               Log out
#======================================================================================
def logout(request):
    #clear session to log out 
    request.session.clear()
    return redirect("registration/logout.html")




