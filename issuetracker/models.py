from django.db import models


# Create your models here.
class User(models.Model):
    name = models.TextField(primary_key=True)
    pin = models.SmallIntegerField(null=False)


class Issue(models.Model):
    reporter = models.ForeignKey(User, primary_key=False, on_delete=models.CASCADE)
    description = models.TextField(primary_key=True)
    status = models.CharField(choices=[("P", "Progreso"), ("R", "Reparado")], default="R", max_length=1)
    report_time = models.DateField(auto_now_add=True)
