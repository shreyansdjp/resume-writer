import sys
from .helpers import check_dates
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import escape
from .models import BasicInfo, Skills, Achievements, WorkExperience, Education

def get_info(request):
    try:
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
        return render(request, 'info/info.html', context)
    except Exception as e:
        print(e)
        return render(request, 'info/info.html', context={})


@login_required(login_url='accounts:login')
def basic_info(request):
    if request.method == "POST":
        contact_no = request.POST['contact_no'] # not required
        website_url = request.POST['website_url'] # not required
        email = request.POST['email']
        linkedin_url = request.POST['linkedin_url']
        address = escape(request.POST['address']) # not required

        # if basic requirement does not meet
        if email == '' and linkedin_url == '':
            messages.error(request, 'You have not entered E-mail and LinkedIn Profile URL')
            return render(request, 'info/info.html')

        # check if the users information is already added
        basic_info = BasicInfo.objects.all().filter(user_id=request.user.id)
        try:
            basic_info = basic_info[0]
        except Exception as e:
            basic_info = BasicInfo()

        # builidng object as we check each datum
        basic_info.user_id = request.user.id
        if email and linkedin_url:
            basic_info.email = email
            basic_info.linkedin_link = linkedin_url

        if contact_no:
            basic_info.contact_no = contact_no

        if website_url:
            basic_info.website_link = website_url

        if address:
            basic_info.address = address

        basic_info.save()
        messages.success(request, 'Basic Information added')
        return redirect('info:get_info')
    else:
        return redirect('info:get_info')


@login_required(login_url='accounts:login')
def education(request):
    if request.method == "POST":
        from_where = request.POST['from_where']
        what = request.POST['what']
        date_started = request.POST['date_started']
        date_ended = request.POST['date_ended'] # not required
        is_going_on = request.POST.getlist('is_going_on')
        grades = request.POST['grades']

        if from_where == '' or date_started == '' or grades == '':
            print(from_where)
            print(date_started)
            print(grades)
            messages.error(request, 'You Forgot to enter the required fields')
            return redirect('info:get_info')

        if date_ended == date_started:
            messages.error(request, 'Date started and ended can\'t be the same')
            return redirect('info:get_info')

        if check_dates(date_started, date_ended):
            messages.error(request, 'Date Format is wrong')
            return redirect('info:get_info')

        edu = ''
        try:
            edu = Education()
        except Exception:
            return redirect('info:get_info')

        try:
            edu.user_id = request.user.id
            edu.from_where = from_where
            edu.what = what
            edu.date_started = date_started
            if is_going_on:
                edu.is_going_on = True
            else:
                edu.date_ended = date_ended
            edu.grade = grades
            edu.save()
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')

        messages.success(request, 'Education Saved!')
        return redirect('info:get_info')
    else:
        return redirect('info:get_info')


@login_required(login_url="accounts:login")
def update_education(request, id):
    if request.method == "POST":
        edu = ''
        try:
            edu = Education.objects.filter(id=id)[0]
        except Exception:
            return redirect('info:get_info')
        if edu.user_id != request.user.id:
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')

        if request.POST.getlist('delete'):
            try:
                edu.delete()
                messages.success(request, 'Education Deleted Successfully')
                return redirect('info:get_info')
            except Exception:
                messages.error(request, 'Something went wrong')
                return redirect('info:get_info')

        from_where = request.POST['from_where']
        what = request.POST['what']
        date_started = request.POST['date_started']
        date_ended = request.POST['date_ended'] # not required
        is_going_on = request.POST.getlist('is_going_on')
        grades = request.POST['grades']

        if from_where == '' or date_started == '' or grades == '':
            messages.error(request, 'You Forgot to enter the required fields')
            return redirect('info:get_info')

        if date_ended == date_started:
            messages.error(request, 'Date started and ended can\'t be the same')
            return redirect('info:get_info')

        if check_dates(date_started, date_ended):
            messages.error(request, 'Date Format is wrong')
            return redirect('info:get_info')

        try:
            edu.from_where = from_where
            edu.what = what
            edu.date_started = date_started
            if is_going_on:
                edu.is_going_on = True
            else:
                edu.date_ended = date_ended
            edu.grade = grades
            edu.save()
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')
        messages.success(request, 'Education Updated Successfully')
        return redirect('info:get_info')
    else:
        return redirect('info:get_info')


@login_required(login_url='accounts:login')
def work_exp(request):
    if request.method == "POST":
        from_where = request.POST['from_where']
        date_started = request.POST['date_started']
        date_ended = request.POST['date_ended'] # not required
        is_going_on = request.POST.getlist('is_going_on')
        time_worked = request.POST['time_worked']
        position = request.POST['position']
        description = request.POST['description']

        if from_where == '' or date_started == '' or time_worked == '' or position == '' or description == '':
            messages.error(request, 'You Forgot to enter the required fields')
            return redirect('info:get_info')

        if date_ended == date_started:
            messages.error(request, 'Date started and ended can\'t be the same')
            return redirect('info:get_info')

        if check_dates(date_started, date_ended):
            messages.error(request, 'Date Format is wrong')
            return redirect('info:get_info')

        work_exp = ''
        try:
            work_exp = WorkExperience()
        except Exception:
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')

        try:
            work_exp.user_id = request.user.id
            work_exp.where = from_where
            work_exp.date_started = date_started
            if is_going_on:
                work_exp.is_going_on = True
            else:
                work_exp.date_ended = date_ended
            work_exp.time_worked = time_worked
            work_exp.description = description
            work_exp.position = position
            work_exp.save()
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')
        messages.success(request, 'Work Experience Saved!')
        return redirect('info:get_info')
    else:
        return redirect('info:get_info')


@login_required(login_url="accounts:login")
def update_work_exp(request, id):
    if request.method == "POST":
        print(request.POST)
        work_exp = ''
        try:
            work_exp = WorkExperience.objects.filter(id=id)[0]
        except Exception:
            return redirect('info:get_info')
        if work_exp.user_id != request.user.id:
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')

        if request.POST.getlist('delete'):
            try:
                work_exp.delete()
                messages.success(request, 'Work Experience Deleted Successfully')
                return redirect('info:get_info')
            except Exception:
                messages.error(request, 'Something went wrong')
                return redirect('info:get_info')

        from_where = request.POST['from_where']
        date_started = request.POST['date_started']
        date_ended = request.POST['date_ended'] # not required
        is_going_on = request.POST.getlist('is_going_on')
        time_worked = request.POST['time_worked']
        position = request.POST['position']
        description = request.POST['description']

        if from_where == '' or date_started == '' or time_worked == '' or position == '' or description == '':
            messages.error(request, 'You Forgot to enter the required fields')
            return redirect('info:get_info')

        if date_ended == date_started:
            messages.error(request, 'Date started and ended can\'t be the same')
            return redirect('info:get_info')

        if check_dates(date_started, date_ended):
            messages.error(request, 'Date Format is wrong')
            return redirect('info:get_info')

        try:
            work_exp.where = from_where
            work_exp.date_started = date_started
            if is_going_on:
                work_exp.is_going_on = True
            else:
                work_exp.date_ended = date_ended
            work_exp.time_worked = time_worked
            work_exp.description = description
            work_exp.position = position
            work_exp.save()
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')
        messages.success(request, 'Work Experience Updated Successfully')
        return redirect('info:get_info')
    else:
        return redirect('info:get_info')


@login_required(login_url='accounts:login')
def achievements(request):
    if request.method == "POST":
        achievement = request.POST['achievement']
        if achievement == '':
            messages.error(request, 'Achievement can\'t be empty')
            return redirect('info:get_info')

        ach = ''
        try:
            ach = Achievements()
        except Exception:
            print(e)
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')

        try:
            ach.user_id = request.user.id
            ach.achievement = achievement
            ach.save()
        except Exception:
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')
        messages.success(request, 'Achievements saved')
        return redirect('info:get_info')
    else:
        return redirect('info:get_info')


@login_required(login_url="accounts:login")
def update_achievements(request, id):
    if request.method == "POST":
        ach = ''
        try:
            ach = Achievements.objects.filter(id=id)[0]
        except Exception:
            return redirect('info:get_info')

        if ach.user_id != request.user.id:
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')

        if request.POST.getlist('delete'):
            try:
                ach.delete()
                messages.success(request, 'Achievement Deleted Successfully')
                return redirect('info:get_info')
            except Exception:
                messages.error(request, 'Something went wrong')
                return redirect('info:get_info')

        achievement = request.POST['achievement']

        if achievement == '':
            messages.error(request, 'Achievement can\'t be empty')
            return redirect('info:get_info')

        try:
            ach.achievement = achievement
            ach.save()
        except Exception:
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')
        messages.success(request, 'Achievement Updated Successfully')
        return redirect('info:get_info')
    else:
         return redirect('info:get_info')



@login_required(login_url='accounts:login')
def skills(request):
    if request.method == "POST":
        skill_name = request.POST['skill_name']
        skill_rating = int(request.POST['skill_rating'])

        if skill_name == '' or skill_rating == '':
            messages.error(request, 'You forgot to enter the required fields')
            return redirect('info:get_info')

        if skill_rating < 1 or skill_rating > 5:
            messages.error(request, 'Rating should be between 1 and 5')
            return redirect('info:get_info')

        skill = ''
        try:
            skill = Skills()
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')

        try:
            skill.user_id = request.user.id
            skill.skill_name = skill_name
            skill.rating = skill_rating
            skill.save()
        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')

        messages.success(request, 'Skills Added Successfully')
        return redirect('info:get_info')
    else:
        return redirect('info:get_info')


@login_required(login_url="accounts:login")
def update_skills(request, id):
    if request.method == "POST":
        skill = ''
        try:
            skill = Skills.objects.filter(id=id)[0]
        except Exception:
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')

        if skill.user_id != request.user.id:
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')

        if request.POST.getlist('delete'):
            try:
                skill.delete()
                messages.success(request, 'Skill Deleted Successfully')
                return redirect('info:get_info')
            except Exception:
                messages.error(request, 'Something went wrong')
                return redirect('info:get_info')

        skill_name = request.POST['skill_name']
        skill_rating = int(request.POST['skill_rating'])

        if skill_name == '' or skill_rating == '':
            messages.error(request, 'You forgot to enter the required fields')
            return redirect('info:get_info')

        if skill_rating < 1 or skill_rating > 5:
            messages.error(request, 'Rating should be between 1 and 5')
            return redirect('info:get_info')

        try:
            skill.skill_name = skill_name
            skill.rating = skill_rating
            skill.save()
        except Exception:
            messages.error(request, 'Something went wrong')
            return redirect('info:get_info')
        messages.success(request, 'Skill Updated Successfully')
        return redirect('info:get_info')
    else:
        return redirect('info:get_info')
