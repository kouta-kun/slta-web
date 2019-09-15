import datetime
import random

import pyodbc
from django.http import HttpRequest, HttpResponse
from django.core import serializers
from django.shortcuts import render
from . import models, forms

# Create your views here.
from django.template import loader

def blog(request: HttpRequest):
    if request.method == "GET":
        template = loader.get_template("public/blog.html")
        quote = random.choice([
            ('No basta un grito para que te escuchen si estás parado entre tanta gente', 'Fernando Santullo'),
            ('No basta un grito para que te escuchen si estás parado entre tanto demente', 'Fernando Santullo'),
            ('Nunca debemos sentirnos satisfechos con nuestros éxitos. '
             'Debemos refrenar la autosatisfacción y criticar constantemente nuestros defectos, '
             'al igual que nos lavamos la cara y barremos el suelo diariamente '
             'para quitar el polvo y mantenerlos limpios', 'Mao Zedong'),
            ('Emboquen el tiro libre, que los buenos volvieron, y están rodando cine de terror.',
             "Carlos 'Indio' Solari")
        ])
        ctx = {'quote_text': quote[0], 'quote_autor': quote[1]}
        return HttpResponse(template.render(ctx, request))

def index(request: HttpRequest):
    if request.method == "GET":
        template = loader.get_template("public/index.html")
        ctx = {}
        return HttpResponse(template.render(ctx, request))


def blogpost(request: HttpRequest):
    if request.method == "GET":
        if request.GET.get("new", None) is not None:
            form = forms.BlogPostForm()
            return render(request, 'public/newBlog.html', {'form': form})
        elif request.GET.get('clear', None) is not None:
            models.BlogPost.objects.all().delete()
            k = models.BlogPost.objects.all()
            return HttpResponse(serializers.serialize('json', k), content_type='application/json')
        else:
            k = models.BlogPost.objects.all()
            return HttpResponse(serializers.serialize('json', k), content_type='application/json')
    elif request.method == "POST":
        form = forms.BlogPostForm(request.POST)
        if form.is_valid():
            newPost = models.BlogPost(titulo=form.cleaned_data["titulo"], markup=form.cleaned_data["texto"],
                                      fecha=datetime.datetime.now())
            newPost.save()
            k = models.BlogPost.objects.all()
            return HttpResponse(serializers.serialize('json', k), content_type='application/json')
        else:
            return render(request, 'public/newBlog.html', {'form': form})
