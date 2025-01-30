from django.contrib import admin
from django.urls import path
from .views import FileUpload

urlpatterns = [
    path('upload/', FileUpload, name='file-upload'),
]
