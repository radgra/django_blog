from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth import logout


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return redirect("blog:index")
    else:
        form = LoginForm()
    return render(request, "login_and_register/login.html", {"form": form})


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_and_register:login")

            # form.save()
    else:
        form = RegisterForm()

    return render(request, "login_and_register/register.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("blog:index")

