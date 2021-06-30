from django.db.models.fields.files import ImageField
from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render #Para usar un template
from seccioneswiki.models import *
from django.contrib import messages


def consultar_articulo(request, id=0):
    try:
        articulos=Article.objects.get(pk=id) # es la consulta SQL con "where id=""
        referencias=Referencias.objects.filter(articulo=articulos.pk)
        enlaces=Enlaces.objects.filter(articulo=articulos.pk)
    except:
        r="Articulo no encontrado"
    return render(request, 'articulo_detalle.html', {
        'articulo':articulos,
        'referencias':referencias,
        'enlaces':enlaces
        })

def consultar_categorias(request , categoria_id):
    categoria= get_object_or_404(Categoria, id=categoria_id)
    articulos_=Article.objects.filter(categorias=categoria_id)
    return render (request, 'categorias.html', {
        'categoria':categoria,
        'articulos':articulos_
    })


def listar_articulos(request):
    articulos=Article.objects.filter(publico='True')
    paginator=Paginator(articulos,5)
    idPaginaPaginador=request.GET.get('page')
    print(f"idPaginaPaginador:{idPaginaPaginador}")
    
    try:
        articulosDePagina = paginator.page(idPaginaPaginador)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articulosDePagina = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articulosDePagina= paginator.page(paginator.num_pages)
    
    return render(request, 'articulos.html', {
        'articulos':articulosDePagina, 
    })

def listar_articulos_random(request):
    articulos=Article.objects.filter(publico='True').exclude(imagen='null').order_by('?')
    
    return render(request, 'carrusel.html', {
        'articulos':articulos, 
    })

def listar_articulos_filtro(request, p_titulo=""):
    q=request.GET.get('p_titulo')
    print(f"____________p_titulo:{q}")
    articulos=Article.objects.filter(titulo__icontains=q) #titulo__exacts  titulo__iexacts !Esto se llama Looups ! 
    
    paginator=Paginator(articulos,5)
    idPaginaPaginador=request.GET.get('page')
    print(f"idPaginaPaginador:{idPaginaPaginador}")
    
    try:
        articulosDePagina = paginator.page(idPaginaPaginador)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articulosDePagina = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articulosDePagina= paginator.page(paginator.num_pages)
    
    return render(request, 'articulos.html', {
        'articulos':articulosDePagina, 
    })


