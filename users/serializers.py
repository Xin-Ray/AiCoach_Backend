from rest_framework import serializers
from .models import User
  # 假设有一个模型用于存储用户的健身目标

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'gender', 'age', 'height', 'weight', 'target_weight', 'experience_level', 'weekly_workouts', 'preferred_equipment', 'workout_goal', 'health_issues']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']



class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        print("Received Password: ", validated_data['password'])
        # 使用 create_user 方法，它会自动调用 set_password 处理密码哈希
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['workout_goal']  # No need for email, we'll get it from the request

    def update(self, instance, validated_data):
        instance.workout_goal = validated_data.get('workout_goal', instance.workout_goal)
        instance.save()
        return instance