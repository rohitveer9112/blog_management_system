from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages
from blogs.models import BlogPost
from .models import Like,Comment
from django import forms
class CommentForm(forms.ModelForm):
 class Meta:model=Comment;fields=['body'];widgets={'body':forms.Textarea(attrs={'rows':3,'placeholder':'Share your thoughts…'})}
@login_required
def like(request,slug):
 if request.method=='POST':
  post=get_object_or_404(BlogPost,slug=slug,status='published');obj,_=Like.objects.get_or_create(user=request.user,post=post)
  if not _:obj.delete()
 return redirect('blogs:detail',slug=slug)
@login_required
def comment(request,slug):
 post=get_object_or_404(BlogPost,slug=slug,status='published')
 if request.method=='POST':form=CommentForm(request.POST)
 else:form=CommentForm()
 if request.method=='POST' and form.is_valid():obj=form.save(commit=False);obj.post=post;obj.author=request.user;obj.save();messages.success(request,'Comment added.');return redirect('blogs:detail',slug=slug)
 messages.error(request,'Please enter a valid comment.');return redirect('blogs:detail',slug=slug)
