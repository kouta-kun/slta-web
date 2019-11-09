from django.db import models


# Create your models here.
class User(models.Model):
    name = models.TextField(primary_key=True)
    pin = models.SmallIntegerField(null=False)


class Update(models.Model):
    codigo_version = models.CharField(max_length=4, primary_key=True)
    fecha_release = models.DateField()
    def nombre_update(self):
        return f"{self.codigo_version} ({self.fecha_release})"

class Issue(models.Model):
    issue_id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey(User, primary_key=False, on_delete=models.CASCADE)
    description = models.TextField(primary_key=False)
    status = models.CharField(choices=[("P", "Progreso"), ("R", "Reparado")], default="P", max_length=1)
    report_time = models.DateField(auto_now_add=True)
    fixed_in = models.ForeignKey(Update, primary_key=False, null=True, default=None, on_delete=models.CASCADE)
