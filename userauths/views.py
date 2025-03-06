from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL # userauths.user -> the model we made

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
    if request.methid == "POST":
        # emial = form = LoginForm(request.POST)
        email = request.POST.get("email") # the email inputed/passed in
        password = request.POST.get("password")
        try:
            # user = User.objects.all() # when you want to take all attributes?
            user = User.objects.get(email=email) # just one attribute -> the email attribute equals the email extracted from thr form
        except:
            messages.warning(request, f"Nu exista utilizatorul cu email-ul {email}")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Utilizator conectat cu succes!")
            return redirect("core:index")
        else:
            messages.warning(request, f"Utilizator negasit")
        context = {

        }
        return redirect(request, "userauths/sign-in.html", context)
    