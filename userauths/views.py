from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

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