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

    ## Logos ##
    logos = Logo.objects.all()
    
    ## Likes ##
    likes = Like.objects.all()

    ## Post for adding logo ##
    if request.method == 'POST':

        ## Taking the values ##
        turma = request.POST.get("turma")
        imagem = request.FILES.get("imagem")

        ## Creating the logo on DB ##
        Logo.createLogo(turma, imagem)

        return redirect(home)

    return render(request, 'home.html', {'logos':logos, 'likes':likes})

@login_required(login_url=loginPage)
def logoffOption(request):
        
    logout(request)

    return redirect(loginPage)

@login_required(login_url=loginPage)
def deletarLogo(request, id):

    Logo.deleteLogo(id)

    return redirect(home)

@login_required(login_url=loginPage)
def curtirLogo(request, id):

    ## Taking the user ##
    user = Usuario.objects.get(cpf=request.user.cpf)

    ## Logo ##
    logo = Logo.objects.get(id=id)

    ## Liking ##
    Like.giveLike(request.user, logo)
    user.liked = 1
    user.save()

    return redirect(home)