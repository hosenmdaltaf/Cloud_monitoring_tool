from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import  User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.forms import UserRegisterForm


# @login_required(login_url ='/')
def homepage(request):
    return render(request, 'account/homepage.html')




def registerview(request):
    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(username = username).first():
            messages.error(request, "This username is already taken")
            return redirect('account:registerpage')

        if password1 != password2 :
            messages.error(request,  'Your password is not same!')
            return redirect('account:registerpage')
        email_exists = User.objects.filter(email=email)
        if email_exists.exists():
            messages.error(request,  'Please select another email this email already in use')
            return redirect('account:registerpage')       
        else:
            newUser=User.objects.create_user(username=username,email=email,password=password1)
            newUser.save()
            messages.success(request,  'Your account has been successfully created')
            return redirect('account:loginpage')
    return render(request,'account/register.html') 

def loginview(request):
    # user =request.user
    # if user.is_authenticated:
    #     return redirect("homepage")
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect('monitoring_app:current_metrics')
            return redirect('account:profile_detail')
        else:
            messages.error(request,  'Something serious happend,please check your username and password is correct!')
    return render(request,'account/login.html') 


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("account:homepage")

@login_required
def profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'account/profile_detail.html', {'profile': profile})

from .models import Profile
from .forms import ProfileForm

@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')  # Redirect to a profile detail page or another relevant page
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'account/update_profile.html', {'form': form})