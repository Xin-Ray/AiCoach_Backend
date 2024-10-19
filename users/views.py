from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import *

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User

class CustomBackend (ModelBackend):
    # 方法重写
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print("try")
            user = User.objects.get(email = username)#|Q ()
            print("user")
            if user.check_password(password):#把密码同user数据库内进行比较
                print("check_password")
                return user
        except Exception as e:
            return None
