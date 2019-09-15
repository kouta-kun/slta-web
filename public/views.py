import datetime

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
        ctx = {}
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
