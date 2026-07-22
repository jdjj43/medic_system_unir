from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")


    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            usuario = authenticate(
                request,
                username=username,
                password=password
            )

            if usuario:

                login(
                    request,
                    usuario
                )

                return redirect(
                    "dashboard"
                )

    else:
        form = LoginForm()

    return render(
        request,
        "usuarios/login.html",
        {
            "form": form
        }
    )

def logout_view(request):

    logout(request)

    return redirect(
        "login"
    )

def dashboard(request):

    return render(
        request,
        "usuarios/dashboard.html"
    )