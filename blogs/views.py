from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .models import BlogPost,Category
from .forms import BlogForm

def listing(request):
 qs=BlogPost.objects.filter(status='published').select_related('author','category');q=request.GET.get('q','').strip();cat=request.GET.get('category','')
 if q:qs=qs.filter(title__icontains=q)|qs.filter(content__icontains=q)
 if cat:qs=qs.filter(category__slug=cat)
 return render(request,'blogs/list.html',{'page_obj':Paginator(qs.distinct(),9).get_page(request.GET.get('page')),'categories':Category.objects.all(),'q':q,'selected_category':cat})
def detail(request,slug):
 post=get_object_or_404(BlogPost.objects.select_related('author','category'),slug=slug,status='published');related=BlogPost.objects.filter(status='published',category=post.category).exclude(pk=post.pk)[:3]
 return render(request,'blogs/detail.html',{'post':post,'related':related})
@login_required
def mine(request):
 qs=BlogPost.objects.filter(author=request.user);return render(request,'blogs/mine.html',{'posts':qs,'counts':{s:qs.filter(status=s).count() for s,_ in BlogPost.Status.choices}})
@login_required
def create(request):return edit_post(request)
@login_required
def edit(request,pk):return edit_post(request,pk)
def edit_post(request,pk=None):
 post=get_object_or_404(BlogPost,pk=pk,author=request.user) if pk else None
 if request.method=='POST':
  form=BlogForm(request.POST,request.FILES,instance=post)
  if form.is_valid():
   obj=form.save(commit=False);obj.author=request.user;action=request.POST.get('action','draft')
   obj.status='pending' if action=='submit' else 'draft';obj.rejection_reason='';obj.published_at=None;obj.save();messages.success(request,'Blog saved and submitted for review.' if obj.status=='pending' else 'Draft saved.');return redirect('blogs:mine')
 else:form=BlogForm(instance=post)
 return render(request,'blogs/editor.html',{'form':form,'post':post})
@login_required
def delete(request,pk):
 post=get_object_or_404(BlogPost,pk=pk,author=request.user)
 if request.method=='POST':post.delete();messages.success(request,'Blog deleted.');return redirect('blogs:mine')
 return render(request,'blogs/delete.html',{'post':post})
