from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserTemplate

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('pages:index')
        else:
            messages.error(request, 'Either username or password is wrong')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']

        # Check if passwords match
        if password == confirm_password:
            print('passwords match')
            # check username
            if User.objects.filter(username=username).exists():
                print('username exists')
                messages.error(request, str(username) + ' is taken')
                return redirect('accounts:register')
            else:
                print('username does not exists')
                if User.objects.filter(email=email).exists():
                    print('email does not exists')
                    messages.error(request, str(email) + ' is already registered')
                    return redirect('accounts:register')
                else:
                    print('everyting is good')
                    # everything is good
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    template = UserTemplate.objects.create(user_id=user.id)
                    template.save()
                    messages.success(request, 'You are successfully registered and now can login')
                    return redirect('accounts:login')
        else:
            print('passwords do not match')
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:register')
    else:
        return render(request, 'accounts/register.html')

@login_required(login_url='accounts:login')
def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'You are now Logged out')
        return redirect('accounts:login')
    return redirect('pages:index')

@login_required(login_url='accounts:login')
def profile(request):
    if request.method == "POST":

        if request.POST.getlist('info'):
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            try:
                user = User.objects.filter(id=request.user.id)[0]
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
            except Exception:
                messages.error(request, 'Something went wrong')
                return redirect('accounts:profile')
            messages.success(request, 'Update the Profile')
            return redirect('accounts:profile')

        if request.POST.getlist('password'):
            old_pass = request.POST['old_pass']
            new_pass = request.POST['new_pass']
            confirm_pass = request.POST['confirm_pass']

            if new_pass != confirm_pass:
                messages.error(request, 'Passwords do not match!')
                return redirect('accounts:profile')

            if not request.user.check_password(old_pass):
                messages.error(request, 'Old Password is wrong!')
                return redirect('accounts:profile')

            try:
                user = User.objects.filter(id=request.user.id)[0]
                user.set_password(new_pass)
                user.save()
            except Exception as e:
                print(e)
                messages.error(request, 'Something went wrong')
                return redirect('accounts:profile')
            messages.success(request, 'Changed the Password.. Please Login again!')
            return redirect('accounts:profile')
    else:
        return render(request, 'accounts/profile.html')

@login_required(login_url='accounts:login')
def dashboard(request):
    if request.method == "POST":
        template_name = request.POST['template_id']
        template_name += '.html'
        user_template = UserTemplate.objects.get(user_id=request.user.id)
        user_template.template_name = template_name
        user_template.save()
        messages.success(request, 'You selected a resume. Now time to enter your information!')
        return redirect('info:get_info')
    else:
        # user_template = UserTemplate.objects.get(user_id=request.user.id)
        # if user_template.template_name != '':
        #     # tell the user which template he/she is selected
        #     return render(request, 'dashboard/' + user_template.template_name)
        try:
            page_number = request.GET['page_no']
            session_number = check_session(request, int(page_number))
            context = {
                'next': str(session_number + 1),
                'prev': str(session_number - 1)
            }
            return render(request, 'dashboard/' + str(request.session['page_number']) + '.html', context)
        except Exception as e:
            session_number = check_session(request)
            context = {
                'next': str(session_number + 1),
                'prev': str(session_number - 1)
            }
            return render(request, 'dashboard/' + str(request.session['page_number']) + '.html', context)

def check_session(request, page_number=1):
    if 'page_number' not in request.session:
        request.session['page_number'] = page_number
        return page_number
    else:
        if page_number > 7 or page_number < 1:
            return int(request.session['page_number'])
        if int(request.session['page_number']) > 7 or int(request.session['page_number']) < 1:
            return int(request.session['page_number'])
        request.session['page_number'] = page_number
        return int(request.session['page_number'])
