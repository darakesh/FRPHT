from django.shortcuts import render , redirect
from django.contrib.auth import logout,login, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from account.models import Account
from account.forms import RegisterForm , LoginForm, UserEditForm
# Create your views here.

def registerview(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Account successfully created!!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'RegisterForm':form, 'btn':'Register', 'clnk':'login'})

def loginview(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(username = email , password = password )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,"Invalid Password or Email!")
    else:
        form = LoginForm()
    return render(request ,'login.html',{'LoginForm':form})

def logoutview(request):
    logout(request)
    return redirect('login')


@login_required
@permission_required('is_superuser')
def createuserview(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'User created successfully!!')
            return redirect('createuser')
    else:
        form = RegisterForm()
    return render(request,'useraccount/users/updateuser.html',{'UserForm':form , 'btn' :'Create','clnk':'home' ,'title':'Create'})


@login_required
def edituserview(request,id):
    user = Account.objects.get(userID=id)
    form = UserEditForm(instance = user)

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            messages.success(request,'User edited successfully!!')
            return redirect('edituser', id=id )

    return render(request,'useraccount/users/updateuser.html',{'UserForm':form , 'btn' :'Save','clnk': 'patientprofile', 'id':id ,'title':'Edit'})


@login_required
@permission_required('is_superuser')
def deleteuserview(request,id):
    user = Account.objects.get(userID=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request,'User deleted successfully!!')
        return redirect('allusers')
    return render(request,'useraccount/users/deleteuser.html',{'user':user, 'id':id})
