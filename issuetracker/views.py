from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from . import models


# Create your views here.
def issues(httpreq):
    temp = loader.get_template("issuetracker/index.html")
    iss = models.Issue.objects.select_related('user').all()
    ctx = {"issues": iss}
    return HttpResponse(temp.render(ctx, httpreq))
