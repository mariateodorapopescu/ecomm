from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm # , LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User
# from django.contrib.auth import logout
# from .forms import LoginForm

# User = settings.AUTH_USER_MODEL # userauths.user -> the model we made

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid(): # the token thing
            new_user = form.save() # it creates new user ig
            username = form.cleaned_data.get("username")
            # email = form.cleaned_data.get("email")
            messages.success(request, f"Adaugare cu succes utilizator {username}")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            print("Inregistrare realizata cu succes")
            return redirect("core:index")
    else:
        print("Nu se poate face inregistrarea")
        form = UserRegisterForm()

    context = {
        # "ceva" : form
        "form" : form
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Utilizator deja conectat!")
        return redirect("core:index")
    
    if request.method == "POST":
        # form = LoginForm(request.POST)
        # if form.is_valid():
        email = request.POST.get("email") # the email passed in
        password = request.POST.get("password")
        try:
            # user = User.objects.all() # when you want to take all attributes?
            user = User.objects.get(email=email) # just one attribute -> the email attribute equals the email extracted from thr form
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Utilizator conectat cu succes!")
                return redirect("core:index")
            else:
                messages.warning(request, "Utilizator negasit")

        except:
            messages.warning(request, f"Nu exista utilizatorul cu email-ul {email}")
        # else:
        #     form = LoginForm()
    #         context = {
    #             # "form": form
    #             "email": email,
    #             "password": password
    #         }
    #         # return redirect(request, "userauths/sign-in.html", context)
    #         return render(request, "userauths/sign-in.html", context)
    # else:
        # return render(request, "userauths/sign-in.html")
    return render(request, "userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, f"Deconectare cu succes!")
    # Verificăm care e numele corect în urls.py pentru view-ul de login
    # Este posibil să fie 'login' sau 'signin' în loc de 'sign-in'
    return redirect("userauths:sign-in")