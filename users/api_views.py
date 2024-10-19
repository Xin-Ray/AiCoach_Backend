from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from rest_framework.permissions import IsAuthenticated
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

class UserRegisterDetail(APIView):
    permission_classes = [AllowAny]  # 允许任何人访问

    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]  # 允许任何人访问

    def post(self, request, *args, **kwargs):
        email = request.data.get('email').lower()  # 确保邮箱为小写
        password = request.data.get('password')

        print(f"Attempting to authenticate user: {email}")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # 如果用户验证成功，获取或创建 token
            token, created = Token.objects.get_or_create(user=user)
            print(f"User authenticated: {user.email}")

            # 返回 token 和成功信息
            return Response({
                'success': True,
                'message': '登录成功',
                'token': token.key  # 返回生成的 token
            }, status=status.HTTP_200_OK)
        else:
            # 如果验证失败，返回错误信息
            print("Authentication failed")
            return Response({
                'success': False,
                'message': '邮箱或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
class GoalView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def post(self, request):
        user = request.user  # Get the logged-in user

        print(f"Authenticated user: {user.email}")
        print(f"Received data: {request.data}")

        serializer = GoalSerializer(user, data=request.data)  # Pass the user instance
        
        if serializer.is_valid():
            serializer.save()  # Update workout_goal for this user
            return Response({'message': 'Workout goal saved successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ExperienceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        experience_level = request.data.get('experience_level')



        # 更新用户的健身经验
        user.experience_level = experience_level
        user.save()

        return Response({'message': 'Experience level saved successfully!'}, status=status.HTTP_201_CREATED)
    
class WeightView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def post(self, request):
        user = request.user
        current_weight = request.data.get('current_weight')
        if current_weight:
            user.current_weight = current_weight
            user.save()
            return Response({'message': 'Weight saved successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    
class TargetWeightView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def post(self, request):
        user = request.user
        target_weight = request.data.get('target_weight')
        if target_weight:
            user.target_weight = target_weight
            user.save()
            return Response({'message': 'Target weight saved successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    
class HeightView(APIView):
    permission_classes = [IsAuthenticated]  # 只允许已认证的用户访问

    def post(self, request):
        user = request.user
        height = request.data.get('height')
        if height:
            user.height = height
            user.save()
            return Response({'message': 'Height saved successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    
class AgeView(APIView):
    permission_classes = [IsAuthenticated]  # 只允许已认证的用户访问

    def post(self, request):
        user = request.user
        age = request.data.get('age')
        if age:
            user.age = age
            user.save()
            return Response({'message': 'Age saved successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class GenderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        gender = request.data.get('gender')

        # 更新用户的健身经验
        user.gender= gender
        user.save()

        return Response({'message': 'Gender saved successfully!'}, status=status.HTTP_201_CREATED)

class HealthIssuesView(APIView):
    permission_classes = [IsAuthenticated]  # 需要用户已登录

    def post(self, request):
        user = request.user  # 获取当前用户
        health_issues = request.data.get('health_issues')  # 获取传递的健康问题

        # 更新用户的 health_issues 字段
        user.health_issues = health_issues
        user.save()

        # 返回成功响应
        return Response({'message': 'Health issues saved successfully!'}, status=status.HTTP_201_CREATED)
   
class WeeklyWorkoutsView(APIView):
    permission_classes = [IsAuthenticated]  # 需要用户已登录

    def post(self, request):
        # 获取当前用户
        user = request.user
        
        # 从请求体中获取 weekly_workouts 参数
        weekly_workouts = request.data.get('weekly_workouts')
        
        # 验证 weekly_workouts 是否存在并有效
        if weekly_workouts is not None and isinstance(weekly_workouts, int) and 0 <= weekly_workouts <= 7:
            # 更新用户的 weekly_workouts 字段
            user.weekly_workouts = weekly_workouts
            user.save()  # 保存更改
            
            # 返回成功响应
            return Response({'message': 'Weekly workouts saved successfully!'}, status=status.HTTP_201_CREATED)
        else:
            # 返回错误响应
            return Response({'error': 'Invalid weekly_workouts value'}, status=status.HTTP_400_BAD_REQUEST)    
        
class MuscleGroupView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def post(self, request):
        user = request.user  # Get the logged-in user
        muscle_groups = request.data.get('muscle_groups')  # Get the passed muscle groups

        # Validate if muscle_groups exists and is a list
        if muscle_groups is not None and isinstance(muscle_groups, list):
            # Update the user's muscle_groups field
            user.muscle_groups = muscle_groups
            user.save()

            # Return a success response
            return Response({'message': 'Muscle groups saved successfully!'}, status=status.HTTP_201_CREATED)
        else:
            # Return an error response if muscle_groups is not valid
            return Response({'error': 'Invalid muscle_groups value'}, status=status.HTTP_400_BAD_REQUEST)