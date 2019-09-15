from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('blogpost', views.blogpost, name='blogpost'),
    path('blog', views.blog, name='blog')
]
