from django.urls import path

from . import views

urlpatterns = [
    path('get_token', views.get_token, name='get_token'),
    path('get_cars', views.get_cars, name='get_cars'),
    path('get_path', views.get_path, name='get_path'),
    path('get_status', views.get_status, name='get_status'),
    path('comment_on', views.comment_on, name='comment_on'),
    path('comments_for', views.comments_for, name='comments_for'),
    path('get_data', views.get_client_data, name='get_data'),
    path('get_gridpath', views.get_gridpath, name='get_gridpath'),
    path('', views.index, name='')
]
