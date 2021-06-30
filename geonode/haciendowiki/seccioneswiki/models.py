from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from django.core.validators import RegexValidator
# Create your models here.

class Category(models.Model):
    nombre=models.CharField(max_length=300)
    nombre_en=models.CharField(max_length=300, verbose_name="Name")
    descripcion= models.TextField(verbose_name="Descripcion", default='null')
    descripcion_en=models.TextField(verbose_name="Description (En)", default='null')
    created_at=models.DateTimeField(auto_now_add=True) #solo cuando se agregue
    updated_at=models.DateTimeField(auto_now=True) #fecha de edicion
    class Meta:
        verbose_name="Category"
        verbose_name_plural="Categorys"
       
    def __str__(self):
        return self.nombre

class Referencies(models.Model):

    nombre=models.CharField(max_length=300, verbose_name="Titulo")
    anno=models.IntegerField(max_length=4, verbose_name="Año de publicación")
    publicador=models.CharField(max_length=300)
    descripcion=models.TextField()
    descripcion_en=models.TextField(verbose_name="Description (En)")
    url= models.URLField(max_length=200, null=True, blank=True, )
    created_at=models.DateTimeField(auto_now_add=True) #solo cuando se agregue
    updated_at=models.DateTimeField(auto_now=True) #fecha de edicion
    class Meta:
        verbose_name="Referencia"
        verbose_name_plural="Referencies"
    def __str__(self):
        return self.nombre



class Article(models.Model):
    #Se pueden revisar tipos de datos en https://docs.djangoproject.com/en/3.1/ref/models/fields/
    titulo = models.CharField(max_length=300, verbose_name="Titulo")
    titulo_en = models.CharField(max_length=300, verbose_name="Title")
    resumen= models.TextField()
    resumen_en= models.TextField(verbose_name="Resume (En)")
    contenido= RichTextField()
    contenido_en= RichTextField()
    publico= models.BooleanField(verbose_name='¿Publicado?')
    imagen=models.ImageField(default='null',upload_to="articulos") #Dentro de la carpeta media
    metadato_imagen= models.TextField()

    categorias=models.ManyToManyField(Category, verbose_name='Categorys', null=True, blank=True)
    referecnias=models.ManyToManyField(Referencies, verbose_name='Referencies', null=True, blank=True)
    
    created_at=models.DateTimeField(auto_now_add=True) #solo cuando se agregue
    updated_at=models.DateTimeField(auto_now=True) #fecha de edicion

    user=models.ForeignKey(User, editable=False, verbose_name='Usuario', on_delete=models.CASCADE)
    
    #Para su visualización en el panel de Django
    class Meta:
        verbose_name="Article"
        verbose_name_plural="Articles"
        ordering=['id']
    def __str__(self):
        return self.titulo


class Links (models.Model):
    url=models.CharField(max_length=1300, verbose_name="URL")
    descripcion=models.CharField(max_length=300, verbose_name="Descripcion",  null=True)
    descripcion_en=models.CharField(max_length=300, verbose_name="Description (En)",  null=True)
    articulo= models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='Enlace')
    created_at=models.DateTimeField(auto_now_add=True) #solo cuando se agregue
    updated_at=models.DateTimeField(auto_now=True) #fecha de edicion
    
    class Meta:
        verbose_name="Enlace"
        verbose_name_plural="Links - URL"
    def __str__(self):
        return self.url