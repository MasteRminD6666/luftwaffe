from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout

from .decorator import unauthenticated_user, allowed_users ,admin_only
from .models import *
from .Forms import OrderForm, CreateUserForm
from .Filter import OrderFilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


@unauthenticated_user
def loginpage(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect ')

        context = {}

        return render(request, 'accounts/login.html', context)

@unauthenticated_user
def register(request):
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                user= form.save()
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Customer.objects.create(
                    user = user
                )
                messages.success ( request , 'Account was created for' + username )
                return redirect('login')

        context = {'form': form}

        return render(request, 'accounts/registration.html', context)


@login_required(login_url='login')
@admin_only
def home(request):

    order = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = order.count()
    delivered = order.filter(status='Delivered').count()
    Pending = order.filter(status='Pending').count()
    context = {'order': order, 'customers': customers, 'total_orders': total_orders, 'total_customers': total_customers,
               'delivered': delivered, 'Pending': Pending}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    Pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'Pending': Pending}
    return render(request, 'accounts/user.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')







@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):

    products = Product.objects.all()
    context = {'Product': products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs
    context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'myfilter': myfilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    Order_form_set = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer= Customer.objects.get(id=pk)
    formset = Order_form_set(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = Order_form_set(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'Order_form': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_Order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'Order_form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {"item": order}
    return render(request, 'accounts/Delete.html', context)
