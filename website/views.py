from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record


def home(request):
    records = Record.objects.all()

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome")
            return redirect("home")
        else:
            messages.error(request, "Not Welcome")
            return redirect("home")
    else:
        return render(request, "home.html", {"records": records})


# def login_user(request):
#     pass


def logout_user(request):
    logout(request)
    messages.success(request, "See ya")
    return redirect("home")


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {"customer_record": customer_record})
    else:
        messages.error(request, "You must be logged to view that page!")
        return redirect("home")
