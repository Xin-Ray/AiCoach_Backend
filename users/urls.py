from django.urls import path
# from .views import register
from . import api_views

urlpatterns = [
    path('register/', api_views.UserRegisterDetail.as_view(), name='register'),
    path('login/', api_views.LoginView.as_view(), name='login'),
    path('save_goal/', api_views.GoalView.as_view(), name='save_goal'),
    path('save_experience/', api_views.ExperienceView.as_view(), name='save_experience'),
    path('save_weight/', api_views.WeightView.as_view(), name='save_weight'),
    path('save_target_weight/', api_views.TargetWeightView.as_view(), name='save_target_weight'),
    path('save_height/', api_views.HeightView.as_view(), name='save_height'),
    path('save_age/', api_views.AgeView.as_view(), name='save_age'),
    path('save_gender/', api_views.GenderView.as_view(),name='save_gender'),
    path('save_health_issues/', api_views.HealthIssuesView.as_view(), name='health_issues'),
    path('save_workouts/', api_views.WeeklyWorkoutsView.as_view(), name='save_workouts'),
    path('save_muscle_groups/', api_views.MuscleGroupView.as_view(), name='save_MuscleGroupView'),

]
