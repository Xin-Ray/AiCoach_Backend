from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.contrib.auth.hashers import make_password

# 定义常量以提高可读性
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]
EXPERIENCE_LEVEL_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]
WORKOUT_GOAL_CHOICES = [
    ('Muscle Gain', 'Muscle Gain'),
    ('Fat Loss', 'Fat Loss'),
    ('Healthy Living', 'Healthy Living'),

]

PLAN_TARGET_CHOICES = [
    ('Muscle Gain', 'Muscle Gain'),
    ('Fat Loss', 'Fat Loss'),
    ('Healthy Living', 'Healthy Living'),
    ('Endurance', 'Endurance'),
    ('Vitality', 'Vitality'),
]
INTENSITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]
TARGET_AREA_CHOICES = [
    ('Arm', 'Arm'),
    ('Back', 'Back'),
    ('Chest', 'Chest'),
    ('Shoulders', 'Shoulders'),
    ('Legs', 'Legs'),
    ('Glutes', 'Glutes'),
    ('Full Body', 'Full Body'),
    ('Abdomen', 'Abdomen'),
]

TARGET_MUSCLE_GROUP_CHOICES = [
    ('Chest', 'Chest'),
    ('Back', 'Back'),
    ('Legs', 'Legs'),
    ('Arms', 'Arms'),
    ('Core', 'Core'),
    ('Full Body', 'Full Body'),
]
DIFFICULTY_LEVEL_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
]
REPORT_TYPE_CHOICES = [
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
    ('Annual', 'Annual'),
]

# 抽象模型基类以减少重复代码
class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')  # 邮箱不能为空
        email = self.normalize_email(email)  # 将邮箱标准化（小写处理）
        print("password: ", password)
        # 使用 make_password 对密码进行加密
        hashed_password = make_password(password)
        
        # 创建用户对象并设置加密后的密码
        user = self.model(email=email, **extra_fields)
        user.password = hashed_password
        
        # 打印加密后的密码（用于调试）
        print("Hashed Password: ", user.password)
        user.save(using=self._db)  # 保存用户到数据库
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # 确保超级用户有 is_staff 权限
        extra_fields.setdefault('is_superuser', True)  # 确保超级用户有 is_superuser 权限

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    current_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    target_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    muscle_groups = models.CharField(max_length=255, choices=TARGET_AREA_CHOICES)
    experience_level = models.CharField(max_length=6, choices=EXPERIENCE_LEVEL_CHOICES, null=True, blank=True)
    weekly_workouts = models.PositiveSmallIntegerField(null=True, blank=True)
    preferred_equipment = models.CharField(max_length=255, null=True, blank=True)
    workout_goal = models.CharField(max_length=20, choices=WORKOUT_GOAL_CHOICES, null=True, blank=True)
    health_issues = models.TextField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(default=True)  # 用户是否活跃
    is_staff = models.BooleanField(default=False)  # 用户是否是管理员
    
    objects = UserManager()  # 自定义的用户管理器

    # 保存前将邮箱转换为小写
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)
   
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

class Login(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField()

class WorkoutPlan(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=255)
    plan_target = models.CharField(max_length=20, choices=PLAN_TARGET_CHOICES)
    target_area = models.CharField(max_length=255, choices=TARGET_AREA_CHOICES)
    intensity = models.CharField(max_length=6, choices=INTENSITY_CHOICES)
    training_course_name = models.CharField(max_length=255, null=True, blank=True)
    lasting_time = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    progress = models.CharField(max_length=255, null=True, blank=True)

class Course(AbstractBaseModel):
    course_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    target_muscle_group = models.CharField(max_length=20, choices=TARGET_MUSCLE_GROUP_CHOICES)
    difficulty_level = models.CharField(max_length=12, choices=DIFFICULTY_LEVEL_CHOICES)
    duration_minutes = models.IntegerField(null=True, blank=True)
    equipment_required = models.CharField(max_length=255, null=True, blank=True)

class UserCourse(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_user_course')
        ]

class AiSuggestion(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion_text = models.TextField()

class Report(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    content = models.TextField()
