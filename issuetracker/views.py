from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from . import models


# Create your views here.
def index(httpreq):
    temp = loader.get_template("issuetracker/index.html")
    iss = models.Issue.objects.select_related('reporter').all()
    ctx = {"issues": iss}
    return HttpResponse(temp.render(ctx, httpreq))
