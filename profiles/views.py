from django.shortcuts import redirect, render
from profiles.forms import SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages



from django.contrib.auth import authenticate, login
from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in")
        return redirect("home")

    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Logged In")
            return redirect('home')
    else:
        form = LoginForm()
    context["form"] = form
    return render(request, "profiles/login_page.html", context)

def logout_view(request):
    logout(request)
    messages.info(request, "Logged Out")
    return redirect("login_view")

def signup(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already Logged in")
        return redirect("home")
    context = {}
    context["form"] = SignUpForm()
    if request.method == 'POST':
        print("request.POST : ", request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, "Submitted form is not valid")
            context["form"] = form
    return render(request, "profiles/signup.html", context)
