from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import User

def flogin_view(request):
    if request.method == "POST":
        user = authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is None:
            return render(request, "users/login.tpl", {"error": "Не верные данные!"})
        else:
            login(request, user)
            return redirect("/user/")

    
    return HttpResponse("ok")


def logout_view(request):
    logout(request)
    return redirect('/login')

def fadduser_view(request):
    if request.method == "POST":
       if request.user.get_group() == "Администратор":
            check_email = len(User.objects.filter(email=request.POST['email']))
            check_username = len(User.objects.filter(username=request.POST['username']))

            if (check_email > 0) or (check_username > 0):
               return render(request, "users/cabinet/add_user.tpl", {"error": "Такие данные уже зарегистрированы!"})
            else:
                selected_group = Group.objects.get(name=request.POST['group'])
                user_object = User.objects.create_user(
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email = request.POST['email'],
                    username = request.POST['username'],
                    password = request.POST['password']
                )
                selected_group.user_set.add(user_object)
                
                return redirect("/user/list")
