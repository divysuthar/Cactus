# from rest_framework import serializers
# from .models import *

# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         fields = '__all__'

# serializers.py
from rest_framework import serializers

class DocumentFileSerializer(serializers.Serializer):
    file = serializers.FileField()