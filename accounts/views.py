from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from blogs.models import BlogPost
from .forms import RegisterForm,ProfileForm,UserDetailsForm
from .models import UserProfile
class UserLoginView(LoginView):template_name='accounts/login.html';authentication_form=AuthenticationForm

def register(request):
 form=RegisterForm(request.POST or None)
 if request.method=='POST' and form.is_valid():user=form.save();UserProfile.objects.get_or_create(user=user);login(request,user);return redirect('accounts:dashboard')
 return render(request,'accounts/register.html',{'form':form})
@login_required
def dashboard(request):
 qs=BlogPost.objects.filter(author=request.user);return render(request,'accounts/dashboard.html',{'counts':{s:qs.filter(status=s).count() for s,_ in BlogPost.Status.choices},'recent':qs[:5]})
@login_required
def profile(request):
 profile,_=UserProfile.objects.get_or_create(user=request.user)
 if request.method=='POST':uf=UserDetailsForm(request.POST,instance=request.user);pf=ProfileForm(request.POST,request.FILES,instance=profile)
 else:uf=UserDetailsForm(instance=request.user);pf=ProfileForm(instance=profile)
 if request.method=='POST' and uf.is_valid() and pf.is_valid():uf.save();pf.save();messages.success(request,'Profile updated.');return redirect('accounts:profile')
 return render(request,'accounts/profile.html',{'user_form':uf,'profile_form':pf})
