from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import UserTemplate
from info.models import BasicInfo, Education, Skills, Achievements, WorkExperience

@login_required(login_url="accounts:login")
def view_template(request):
    try:
        user_template = UserTemplate.objects.filter(user_id=request.user.id)[0]
        basic_info = BasicInfo.objects.all().filter(user_id=request.user.id)[0]
        skills = Skills.objects.all().filter(user_id=request.user.id)
        achievements = Achievements.objects.all().filter(user_id=request.user.id)
        experiences = WorkExperience.objects.all().filter(user_id=request.user.id)
        educations = Education.objects.all().filter(user_id=request.user.id)
        context = {
            'basic_info': basic_info,
            'skills': skills,
            'achievements': achievements,
            'experiences': experiences,
            'educations': educations
        }
        return render(request, 'view/' + str(user_template.template_name), context)
    except Exception as e:
        print(e)
        messages.error(request, 'Before Viewing.. Please enter atleast one information in every field')
        return redirect('info:get_info')
