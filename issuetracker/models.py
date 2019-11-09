from django.db import models


# Create your models here.
class User(models.Model):
    name = models.TextField(primary_key=True)
    pin = models.SmallIntegerField(null=False)


class Issue(models.Model):
    reporter = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(choices=[("P", "Progreso"), ("R", "Reparado")], default="R")
    report_time = models.DateField(auto_now_add=True, auto_now=True)
