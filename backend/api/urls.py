from django.contrib import admin
from django.urls import path
from .views import summarize_document

urlpatterns = [
    path('upload/', summarize_document, name='file-upload'),
    # path('click/', TestAPI, name='check'),
]
