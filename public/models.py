from django.db import models


# Create your models here.
class BlogPost(models.Model):
    titulo = models.fields.TextField(null=False, blank=False, primary_key=True, max_length=50)
    fecha = models.fields.DateTimeField(null=False, blank=False)
    markup = models.fields.TextField(null=False, blank=False)
    tags = models.fields.TextField(null=False, default="")
