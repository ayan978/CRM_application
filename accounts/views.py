from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

from .models import *
from .forms import OrderForm, UserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'Username or Password is incorrect!')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def register(request):       
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, 'User created successfully!')
            return redirect('login')

        else:
            messages.error(request, 'Sorry! Something went wrong.')

    context = {'user_form' : user_form}
    return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()

    context = {'customers' : customers, 'orders' : orders, 'total_customers' : total_customers, 'total_orders' : total_orders, 'delivered' : delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {'products' : products}
    return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    filter1 = OrderFilter(request.GET, queryset=orders)
    orders = filter1.qs
    context = {'customer' : customer, 'orders' : orders, 'total_orders' : total_orders, 'filter1':filter1}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})

    if request.method=='POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order1 = Order.objects.get(id=pk)
    form = OrderForm(instance=order1)

    if request.method=='POST':
        form1 = OrderForm(request.POST, instance=order1)
        if form1.is_valid():
            form1.save()
            return redirect('/')
    context = {'form':form}

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order1 = Order.objects.get(id=pk)
    context = {'order1' : order1}
    
    if request.method == 'POST':
        order1.delete()
        return redirect('/')
        
    return render(request, 'accounts/delete_record.html', context)


