from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
# Create your views here.

from .models import *
from .forms import OrderForm
from .filters import OrderFilter

def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()

    context = {'customers' : customers, 'orders' : orders, 'total_customers' : total_customers, 'total_orders' : total_orders, 'delivered' : delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    context = {'products' : products}
    return render(request, 'accounts/products.html', context)

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    filter1 = OrderFilter(request.GET, queryset=orders)
    orders = filter1.qs
    context = {'customer' : customer, 'orders' : orders, 'total_orders' : total_orders, 'filter1':filter1}
    return render(request, 'accounts/customer.html', context)

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


def deleteOrder(request, pk):
    order1 = Order.objects.get(id=pk)
    context = {'order1' : order1}
    
    if request.method == 'POST':
        order1.delete()
        return redirect('/')
        
    return render(request, 'accounts/delete_record.html', context)


