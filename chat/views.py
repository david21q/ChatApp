from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm 
from .forms import ChangeUsernameForm

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chatPage.html", context)

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # create the new user
            login(request, user)  # log the user in after registration
            return redirect("chat-page")
    else:
        form = RegistrationForm() 

    return render(request, "registerUser.html", {"form": form})

def profile_settings(request): # Update current user
    if not request.user.is_authenticated:
        return redirect("login_user") 

    if request.method == "POST":
        form = ChangeUsernameForm(request.POST, instance=request.user)  
        if form.is_valid():
            form.save() 
            return redirect("chat-page")  
    else:
        form = ChangeUsernameForm(instance=request.user) 

    return render(request, "ProfileSettings.html", {"form": form})
