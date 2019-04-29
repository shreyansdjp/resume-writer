from django.urls import path
from . import views

app_name = 'view'
urlpatterns = [
    path('', views.view_template, name='view_template')
]
