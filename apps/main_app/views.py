from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
import bcrypt, datetime

def registration(request):
  if request.session.session_key:
    print request.session.session_key, User.objects.count()
  return render(request, 'main_app/registration.html')

def login(request):
  errors = User.objects.validator(request.POST)
  if len(errors):
    for tag, error in errors.iteritems():
      messages.error(request, error, extra_tags=tag)
    return redirect('/registration')
  else:
    request.session['current_user_id'] = User.objects.filter(email=request.POST['email'])[0].id
    return redirect('/index')

def create(request):
  errors = User.objects.validator(request.POST)
  if len(errors):
    for tag, error in errors.iteritems():
      messages.error(request, error, extra_tags=tag)
    return redirect('/registration')
  else:
    encrypted = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(name=request.POST['name'],email=request.POST['email'],date_hired=request.POST['date_hired'],password=encrypted)
    if bcrypt.checkpw(request.POST['password_confirm'].encode(), encrypted.encode()):

      user.save()
      request.session['current_user_id'] = User.objects.filter(email=request.POST['email'])[0].id
      return redirect('/index')
    else:
      return redirect('/registration')

def index(request):
  if type(request.session.session_key) == str:

    if Product.objects.exists():
      wish_list = Wish_List.objects.filter(user_id=User.objects.filter(id=request.session['current_user_id'])[0].id)
      context = {
        'users': User.objects.all(),
        'products': Product.objects.all(),
        'current_user': User.objects.filter(id=request.session['current_user_id'])[0],
        'user_products': Product.objects.filter(creator=User.objects.filter(id=request.session['current_user_id'])),
        'wish_list': Wish_List.objects.filter(user_id=User.objects.filter(id=request.session['current_user_id'])),
        # 'product': Product.objects.filter(id=Wish_List.objects.filter(id=wish_list)[0].product_id)
      }
    else: 
      context = {
      'users': User.objects.all(),
      'current_user': User.objects.filter(id=request.session['current_user_id'])[0]
      }

    return render(request, 'main_app/index.html', context)
  else:
    return redirect('/registration')

def add_to_wishlist(request):
  current_user_id = request.session['current_user_id']
  wishlist_object = Wish_List.objects.create(user_id=current_user_id, product_id = Product.objects.get(product_name=request.POST['name']).id)
  return redirect('/index')

def remove_from_wishlist(request):
  current_user_id = request.session['current_user_id']
  wishlist_object = Wish_List.objects.filter(user_id=current_user_id, product_id = Product.objects.get(product_name=request.POST['name']).id).delete()
  return redirect('/index')

def delete_product(request):
  current_user_id = request.session['current_user_id']
  product = Product.objects.filter(id=request.POST['id'],creator=User.objects.get(id=current_user_id))
  product.delete()
  return redirect('/index')

def new(request):
  if type(request.session.session_key) == str:
    return render(request,'main_app/new.html')
  else:
    return redirect('/registration')

def make_product(request):
  current_user_id = request.session['current_user_id']
  print request.POST['product_name']
  if len(request.POST['product_name']) > 3:
    product = Product.objects.create(product_name=request.POST['product_name'], creator=User.objects.filter(id=current_user_id)[0])
    wishlist_object = Wish_List.objects.create(user_id=User.objects.filter(id=current_user_id)[0].id, product_id = Product.objects.filter(product_name=request.POST['product_name'])[0].id)
    return redirect('/index')
  else:
    return redirect('/index')



def show(request):
  product_id = Wish_List.objects.get(product_id=request.GET['id'])
  context = {
    'product': Product.objects.get(id=product_id)
  }
  return redirect('/show/<int:product_id>')

def logout(request):
    request.session.flush()
    return redirect('/registration')
