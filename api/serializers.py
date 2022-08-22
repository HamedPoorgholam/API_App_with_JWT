from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from . models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['username','email','password']