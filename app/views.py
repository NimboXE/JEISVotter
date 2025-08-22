from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from app.models import *

# Create your views here.
def loginPage(request):

    ## Login ##
    if request.method == 'POST':

        try:
            cpf = request.POST.get("cpf")
            password = request.POST.get("password")

            ## Getting user's object for username ##
            userObject = Usuario.objects.get(cpf=cpf)

            ## Authenticating the user ##
            user = authenticate(request, username=userObject.username, password=password)

            ## Authenticating the existence and loginning the user ##
            if user is not None:
                login(request, user)

                return redirect(home)
            
        except:
            return redirect(loginPage)

    return render(request, 'sesi_login_page.html')

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

    return render(request, 'sesi_senai_signup.html')

@login_required(login_url=loginPage)
def home(request):

    ## Logos ##
    logos = Logo.objects.all()
    
    ## Dashboard ##
    likes = []
    users = Usuario.objects.all()
    usersCount = users.count()
    usersLiked = 0
    mostLikedClasses = []

    ## Filling the likes array 
    for logo in logos:
        likes.append(logo.likes)

        mostLiked = max(likes)
    
    ## UsersLiked
    for user in users:
        if user.liked == 1:
            usersLiked += 1

    ## Filling the mostLikedClasses
    for logo in logos:
        if logo.likes == mostLiked:
            mostLikedClasses.append(logo)

    ## Post for adding logo ##
    if request.method == 'POST':

        ## Taking the values ##
        turma = request.POST.get("turma")
        imagem = request.FILES.get("imagem")

        ## Creating the logo on DB ##
        Logo.createLogo(turma, imagem)

        return redirect(home)

    return render(request, 'jeis_logo_viewer.html', {'logos':logos, 'usersLiked':usersLiked, 'usersCount':usersCount, 'mostLikedClasses':mostLikedClasses})

@login_required(login_url=loginPage)
def logoffOption(request):
        
    logout(request)

    return redirect(loginPage)

@login_required(login_url=loginPage)
def deletarLogo(request, id):

    Logo.deleteLogo(id)
    user = Usuario.objects.get(cpf=request.user.cpf)
    user.liked = 0
    user.save()

    return redirect(home)

@login_required(login_url=loginPage)
def curtirLogo(request, id):

    ## Taking the user ##
    user = Usuario.objects.get(cpf=request.user.cpf)

    ## Logo ##
    logo = Logo.objects.get(id=id)

    ## Liking ##
    Like.giveLike(request.user, logo)
    logo.likes += 1
    logo.save()
    user.liked = 1
    user.save()

    return redirect(home)

@login_required(login_url=loginPage)
def editarLogo(request, id):

    logo = Logo.objects.get(id=id)

    if request.method == "POST":

        imagem = request.FILES.get("imagem")
        turma = request.POST.get("turma")

        logo.turma = turma
        logo.imagem = imagem

        logo.save()

        return redirect(home)

    return render(request, 'editarLogo.html', {'logo':logo})