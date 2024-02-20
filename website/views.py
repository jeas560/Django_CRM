from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
from .forms import AddRecordForm


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


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted sucessfully!")
    else:
        messages.error(request, "You must be logged to do that")
    return redirect("home")


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record added sucessfully!")
                return redirect("home")
        return render(request, "add_record.html", {'form':form})
    else:
        messages.error(request, "You must be logged to do that")
        return redirect("home")

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated sucessfully!")
            return redirect("home")
        return render(request, "update_record.html", {'form':form})
    else:
        messages.error(request, "You must be logged to do that")
        return redirect("home")