from django.shortcuts import render
from blogs.models import BlogPost,Category

def home(request):return render(request,'core/home.html',{'featured':BlogPost.objects.filter(status='published').select_related('author','category')[:1],'latest':BlogPost.objects.filter(status='published').select_related('author','category')[:6],'categories':Category.objects.all()[:8]})
def about(request):return render(request,'core/about.html')
