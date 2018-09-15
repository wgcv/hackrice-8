from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, TransactionForm
from .models import DataUser, Transaction
# Create your views here.

def login(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'create.html', {
        'form': form
    })

def home(request):
    return render(request, 'home.html')

def logoutView(request):
    logout(request)
    return redirect('/')

def createUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            dataUser = DataUser.objects.create(user = user)
            dataUser.save()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'create.html', {
        'form': form
    })


@login_required
def dashboard(request):
    datauser = DataUser.objects.get(user = request.user)
    history = Transaction.objects.filter(user = request.user).order_by('-date')[:10]
    return render(request, 'dashboard.html', {'datauser': datauser, 'history':history})

@login_required
def operations(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            datauser = DataUser.objects.get(user = request.user)
            datauser.amount = datauser.amount + transaction.amount
            return redirect('dashboard')
        else:
            return redirect('opeation')
    else:
        form = TransactionForm()
    return render(request, 'operation.html', {
        'form': form
    })