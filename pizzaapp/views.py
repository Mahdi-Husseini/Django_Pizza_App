import imp
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import OrderModel, PizzaModel, CustomerModel
# Create your views here.

def adminloginview(request):
    return render(request,"adminlogin.html")

def authenticateadmin(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username = username, password = password)

    #user exists
    if user is not None and user.username == "admin":
        login(request, user)
        return redirect('adminhomepage')

    #user doesn't exists
    if user is None:
        messages.add_message(request, messages.ERROR, "invalid username or password")
        return redirect('adminloginpage')


def adminhomepageview(request):
    context = {'pizzas' : PizzaModel.objects.all()}
    return render(request,"adminhomepage.html", context)

def logoutadmin(request):
    logout(request)
    return redirect("adminloginpage")

def addpizza(request):
    name = request.POST['pizza']
    price = request.POST['price']
    PizzaModel(name = name, price = price).save()
    return redirect("adminhomepage")

def deletepizza(request, pizzapk):
    PizzaModel.objects.filter(id = pizzapk).delete()
    return redirect("adminhomepage")

def homepageview(request):
    return render(request, "homepage.html")

def signupuser(request):
    username = request.POST['username']
    password = request.POST['password']
    phone =  request.POST['phone']

    if User.objects.filter(username = username).exists():
        messages.add_message(request, messages.ERROR, "ay yo, your name exists!")
        return redirect("homepage")

    User.objects.create_user(username=username, password=password).save()
    lastobject = len(User.objects.all()) - 1
    CustomerModel(userid = User.objects.all()[int(lastobject)].id, phone = phone).save()
    messages.add_message(request, messages.ERROR, f"Yo wassup {username}!")
    return redirect("homepage")

def userloginview(request):
    return render(request, "userlogin.html")

def logoutuser(request):
    logout(request)
    return redirect("homepage")

def customerwelcomeview(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    username = request.user.username
    context = {'username' : username, 'pizzas' : PizzaModel.objects.all()}
    return render(request, "customerpage.html", context)

def authenticateuser(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username = username, password = password)

    #user exists
    if user is not None:
        login(request, user)
        return redirect('customerpage')

    #user doesn't exists
    if user is None:
        messages.add_message(request, messages.ERROR, "Yo, you look kinda sus!?")
        return redirect('userlogin')


def placeorder(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    username = request.user.username
    phone = CustomerModel.objects.filter(userid = request.user.id)[0].phone
    address = request.POST['address']
    ordereditems = ""
    for pizza in PizzaModel.objects.all():
        pizzaid = pizza.id
        name = pizza.name
        price = pizza.price
        quantity = request.POST.get(str(pizzaid), "")
        if str(quantity) != "0" and str(quantity) != "":
            ordereditems += name + " " + str(int(price)*int(quantity)) + "$ quantity: " + quantity + "|     "
    
    if ordereditems == "":
        messages.add_message(request, messages.WARNING, "Kermel allah order something")
        return redirect("customerpage") 

    messages.add_message(request, messages.SUCCESS, "Pizza is on its way!")
    OrderModel(username = username, phone = phone, address = address, ordereditems = ordereditems).save()
    return redirect('customerpage')


def userorders(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    orders = OrderModel.objects.filter(username = request.user.username)
    context = {'orders' : orders}
    return render(request, "userorders.html", context)

def adminorders(request):
    if not request.user.is_superuser:
        return redirect("adminloginpage")
    orders = OrderModel.objects.all()
    context = {'orders' : orders}
    return render(request, "adminorders.html", context)

def acceptorder(request, orderpk):
    order = OrderModel.objects.filter(id = orderpk)[0]
    order.status = "accepted"
    order.save()
    return redirect(request.META['HTTP_REFERER'])

def declineorder(request, orderpk):
    order = OrderModel.objects.filter(id = orderpk)[0]
    order.status = "rejected"
    order.save()
    return redirect(request.META['HTTP_REFERER'])  
