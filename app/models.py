from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):

    ## Atributes ##
    cpf = models.CharField(max_length=11, null=False, blank=False, primary_key=True)
    liked = models.BooleanField(null=False, blank=False, default=0)

    ## Methods ##
    @classmethod
    def createUser(cls, username, password, email, cpf):
        return cls.objects.create_user(username=username, password=password, email=email, cpf=cpf)

class Logo(models.Model):

    ## Atributes ##
    turma = models.CharField(max_length=40, null=False, blank=False)
    imagem = models.FileField(null=False, blank=False)
    likes = models.IntegerField(null=False, blank=False, default=0)

    ## Methods ##
    @classmethod
    def createLogo(cls, turma, imagem):
        return cls.objects.create(turma=turma, imagem=imagem)
    
    #
    @classmethod
    def editLogo(cls, id, turma, imagem):

        ## Getting object ##
        logo = cls.objects.get(id=id)

        ## Editing the object ##
        logo.turma = turma
        logo.imagem = imagem

        ## Saving the object ##
        logo.save()

    #
    @classmethod
    def deleteLogo(cls, id):
        return cls.objects.get(id=id).delete()
    
class Like(models.Model):

    ## Atributes ##
    logo = models.ForeignKey(Logo, on_delete=models.CASCADE)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    ## Methods ##
    @classmethod
    def giveLike(cls, user, logo):
        return cls.objects.create(logo=logo, user=user)