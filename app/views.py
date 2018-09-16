from django.shortcuts import render
from django.shortcuts import redirect

from decimal import *

from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from math import sqrt
from .forms import SignUpForm, TransactionForm, SpecialTransactionForm
from .models import DataUser, Transaction, Message, MessageDescription
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
    if request.user.is_authenticated:
        return redirect('dashboard')

    else:
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
    history = Transaction.objects.filter(user = request.user).order_by('-date')
    if(datauser.progress > 0):
        progress = (datauser.progress / (datauser.next_progress )) * 100
    else:
        progress = 0
    if (Message.objects.filter(user = request.user).count()):
        message = Message.objects.filter(user = request.user)
        if( len(message) > 0):
            message = message[0]
            message.delete()
    else:
        message = None
    return render(request, 'dashboard.html', {'datauser': datauser, 'history':history, 'progress': int(progress), 'message': message})

@login_required
def operations(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            if(transaction.type_transaction != 'DP' and  transaction.type_transaction != 'LO' ):

                transaction.amount = transaction.amount  * -1
            datauser = DataUser.objects.get(user = request.user)
            if(datauser.amount + transaction.amount >= 0):
                datauser.amount = datauser.amount + transaction.amount
                transaction.save()
                datauser.save()
                check(request, transaction)
                progress(request, transaction, 100)
            else:
                return render(request, 'error.html')
            return redirect('dashboard')
        else:
            return render(request, 'error.html')
    else:
        form = TransactionForm()
    return render(request, 'operation.html', {
        'form': form
    })

@login_required
def message(request, id):
    message = MessageDescription.objects.get(pk = id)
    return render(request, 'message.html', {'message': message})

@login_required
def faq(request):
    messages = MessageDescription.objects.all()
    return render(request, 'faq.html', {'messages': messages})

@login_required
def prices(request):
    return render(request, 'prizes.html')



@login_required
def doit(request):
    if request.method == 'POST':
        form = SpecialTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            if(transaction.type_transaction != 'DP' and  transaction.type_transaction != 'LO' ):
                transaction.amount = transaction.amount  * -1
            datauser = DataUser.objects.get(user = request.user)
            if(datauser.amount + transaction.amount >= 0):
                datauser.amount = datauser.amount + transaction.amount
                transaction.save()
                datauser.save()
                check(request, transaction)
                progress(request, transaction, 0)
            else:
                return render(request, 'error.html')
            return redirect('dashboard')
        else:
            return render(request, 'error.html')
    else:
        form = SpecialTransactionForm()
    return render(request, 'doit.html', {
        'form': form
    })
def check(request, transaction):
    datauser = DataUser.objects.get(user = request.user)
    how_many = Transaction.objects.filter(user = request.user).count()
    avg = Transaction.objects.filter(user = request.user).aggregate(avg = Avg('amount'))['avg']
    last_3_transactions = Transaction.objects.filter(user = request.user).order_by('-date')[:3]
    if(last_3_transactions[0].amount < 0 and last_3_transactions[1].amount < 0 and last_3_transactions[2].amount < 0):
        message = Message(message=MessageDescription.objects.get(id=3), user = request.user)
        message.save()
    if(transaction.amount > avg):
        message = Message(message=MessageDescription.objects.get(id=4), user = request.user)
        message.save()
    if(how_many < 2):
        message = Message(message=MessageDescription.objects.get(id=2) , user = request.user)
        message.save()
    if(datauser.amount > 100000):
        message = Message(message=MessageDescription.objects.get(id=5), user = request.user)
        message.save()

def progress(request, transaction, points):
    datauser = DataUser.objects.get(user = request.user)
    total = Decimal(datauser.next_progress)
    add = Decimal(0)
    if(transaction):
        if(transaction.amount > 0):
            add = add + transaction.amount * Decimal(0.10)
        add = add + Decimal(20)
    add = add + Decimal(points)
    while((datauser.progress+add) >= total):
        datauser.level = datauser.level+1
        add = -1* (total-((datauser.progress+add)))
        print(add)
        datauser.progress = 0
        datauser.next_progress = total * Decimal(1.25)
        total = datauser.next_progress
    if((datauser.progress+add)<total):
        if(add >0):
            datauser.progress = datauser.progress + add
    datauser.save()