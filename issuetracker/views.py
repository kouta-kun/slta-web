from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.template import loader
from . import models


# Create your views here.
def index(httpreq: HttpRequest):
    if httpreq.method == 'GET':
        temp = loader.get_template("issuetracker/index.html")
        iss = models.Issue.objects.select_related('reporter').all()
        ctx = {"issues": iss}
        return HttpResponse(temp.render(ctx, httpreq))
    elif httpreq.method == 'POST':
        user = httpreq.POST['user']
        user = models.User.objects.get(name=user)
        pin = httpreq.POST['pin']
        if user.pin != pin:
            return HttpResponse("PIN incorrecto", status=403)
        message = httpreq.POST['desc']
        models.Issue(reporter=user, description=message).save()
