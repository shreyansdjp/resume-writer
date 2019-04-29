from django.urls import path
from . import views

app_name = 'info'
urlpatterns = [
    path('', views.get_info, name='get_info'),
    path('basic_info/', views.basic_info, name='basic_info'),
    path('education/', views.education, name='education'),
    path('education/<int:id>', views.update_education, name="update_education"),
    path('work_exp/', views.work_exp, name='work_exp'),
    path('work_exp/<int:id>', views.update_work_exp, name="update_work_exp"),
    path('achievements/', views.achievements, name='achievements'),
    path('achievements/<int:id>', views.update_achievements, name='update_achievements'),
    path('skills/', views.skills, name='skills'),
    path('skills/<int:id>', views.update_skills, name='update_skills'),
]
