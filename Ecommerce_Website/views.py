import requests
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse
# Part authentication ( login - logout) ------------------------
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
# ---------------------------------------------------------------
# Part Register 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Q
from .forms import SignUpForm, UpadteUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

import json
from cart.cart import Cart



# Create your views here.

def materiel_HOME(request):
    products = produit.objects.all()
    return render(request, 'Ecom/index.html',{'products':products})

def home(request):
    return render(request, 'home.html')

def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('Nom')       
        email = request.POST.get('email')
        objt = request.POST.get('Objet')
        msg = request.POST.get('Message')
        data = contactUs(name=nom, mail=email, objet=objt, message=msg)
        data.save()

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def materiel_home(request):
    categorie = categories.objects.all()
    produits = produit.objects.all()  # Récupère tous les produits
    return render(request, 'materiel.html', {'produits': produits, 'categorie': categorie})

# def product_detail(request, id):
#     produit_detail = get_object_or_404(produit, id=id)
#     return render(request, 'deatil.html', {'produit': produit_detail})


def category_summary(request):
    category = categories.objects.all()
    return render(request, 'Ecom/category_summary.html',{'category': category})

# Product ----------------------------
def product(request, pk):
    product = produit.objects.get(id=pk)
    return render(request, 'Ecom/product.html',{'products':product})


def category(request, foo):
    # foo = foo.replace('-', ' ')
    try:
        category = categories.objects.get(name_cat=foo)
        products =  produit.objects.filter(categorie=category)
        return render(request, 'Ecom/category.html',{'products':products, 'category': category})
    except:
        messages.success(request, ("That Category Doesn't exists"))
        return redirect('base')





# Login --- Logout [ views ] ---------------------
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Do some Shopping cart Stuff 
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # convert daatabse string to python dictionary
            if saved_cart:
                # convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                # get the cart
                cart = Cart(request)
                # Loop thru the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, (f"You Have Been Logged, welcome {username}"))
            return redirect('base')
        else: 
            messages.success(request, ("Error... ,Try Agaiinnnn"))
            return redirect('login')
    else:
        return render(request, 'Ecom/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out... Thanks for Shoping"))
    return redirect('base')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, (f"You Have Been Registered, Welcome {username}"))
            return redirect('base')
        else:
            messages.success(request, ("Error... ,Try Agaiinnnn"))
            return redirect('register')
    else:
        return render(request, 'Ecom/register.html',{'form': form})
# --------------------------------------------------------
    



# Upadte [ Profile --- Password ]--------------------------------------------
    
def update_info(request):
    if request.user.is_authenticated:
        # Get Current User ------------------
        current_user = Profile.objects.get(user__id=request.user.id)
        # current_user, created = Profile.objects.get_or_create(user=request.user)
        # Get Current User's Shipping Info ------------------
        shipping_user, created = ShippingAddress.objects.get_or_create(user__id=request.user.id)

        # Get original User Form ------------------
        form = UserInfoForm(request.POST or None, instance=current_user)

        # Get User's Shipping Form ------------------
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            # Save original Form
            form.save()
            # Save Shipping form
            shipping_form.save()
            messages.success(request, ("Your Info Has Been Has Been Updated!!!"))
            return redirect('base')
        
        return render(request, 'Ecom/update_info.html',{'form': form,'shipping_form':shipping_form})
    else:
        messages.success(request, ("You Must Be Logged In To Access That Page !!!"))
        return redirect('base')



# | Profile |_________
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        update_user_form = UpadteUserForm(request.POST or None, instance=current_user)
        if update_user_form.is_valid():
            update_user_form.save()

            login(request, current_user)
            messages.success(request, ("Users Has Been Updated!!!"))
            return redirect('base')
        
        return render(request, 'Ecom/update_user.html',{'update_user_form': update_user_form})
    else:
        messages.success(request, ("You Must Be Logged In To Access That Page !!!"))
        return redirect('base')




# | Password |_________
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("You Password Has Been Updated"))
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error) 
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'Ecom/update_password.html',{'form': form})
    else:
        messages.success(request, ("You Must Be Logged In To Access That Page !!!"))



# search 
def search(request):
    # Determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # Query The Products DB Model
        searched = produit.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        # test for null
        if not searched:
            messages.success(request, ("No Product Found"))
            return render(request,"Ecom/search.html", {})
        else:
            return render(request, 'Ecom/search.html',{'searched':searched})
    else:
        return render(request, 'Ecom/search.html',{})