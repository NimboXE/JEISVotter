from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from app.models import *

# Create your views here.
def loginPage(request):

    ## Login ##
    if request.method == 'POST':
        cpf = request.POST.get("cpf")
        password = request.POST.get("password")

        print(cpf, password)

        ## Getting user's object for username ##
        userObject = Usuario.objects.get(cpf=cpf)

        ## Authenticating the user ##
        user = authenticate(request, username=userObject.username, password=password)
        print(user)

        ## Authenticating the existence and loginning the user ##
        if user is not None:
            login(request, user)

            return redirect(home)

    return render(request, 'loginPage.html')

def signupPage(request):

    ## SignUp ##
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        password = request.POST.get("password")

        ## Creating the user ##
        Usuario.createUser(username, password, email, cpf)

        return redirect(loginPage)

    return render(request, 'signupPage.html')

@login_required(login_url=loginPage)
def home(request):
    return render(request, 'home.html')

@login_required(login_url=loginPage)
def logoffOption(request):
        
    logout(request)

    return redirect(loginPage)