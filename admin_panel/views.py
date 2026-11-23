from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from blogs.models import BlogPost,Category
from blogs.forms import CategoryForm
from interactions.models import Comment
from contact.models import ContactMessage
@staff_member_required
def dashboard(request):return render(request,'admin_panel/dashboard.html',{'user_count':User.objects.count(),'post_count':BlogPost.objects.count(),'published_count':BlogPost.objects.filter(status='published').count(),'pending_count':BlogPost.objects.filter(status='pending').count(),'rejected_count':BlogPost.objects.filter(status='rejected').count(),'category_count':Category.objects.count(),'comment_count':Comment.objects.count(),'recent_users':User.objects.order_by('-date_joined')[:6],'recent_posts':BlogPost.objects.select_related('author').order_by('-created_at')[:8]})
@staff_member_required
def posts(request):
 qs=BlogPost.objects.select_related('author','category').order_by('-created_at');status=request.GET.get('status','')
 if status:qs=qs.filter(status=status)
 return render(request,'admin_panel/posts.html',{'posts':qs,'selected':status,'choices':BlogPost.Status.choices})
@staff_member_required
@require_POST
def moderate(request,pk,decision):
 post=get_object_or_404(BlogPost,pk=pk)
 if post.status!='pending':messages.error(request,'Only pending posts can be moderated.')
 elif decision=='approve':post.status='published';post.published_at=timezone.now();post.rejection_reason='';post.save();messages.success(request,'Post published.')
 elif decision=='reject':
  reason=request.POST.get('reason','').strip()
  if not reason:messages.error(request,'A rejection reason is required.')
  else:post.status='rejected';post.rejection_reason=reason;post.published_at=None;post.save();messages.success(request,'Post rejected.')
 return redirect('admin_panel:posts')
@staff_member_required
def users(request):return render(request,'admin_panel/users.html',{'users':User.objects.order_by('-date_joined')})
@staff_member_required
@require_POST
def toggle_user(request,pk):
 u=get_object_or_404(User,pk=pk)
 if u.is_superuser:messages.error(request,'Superuser cannot be deactivated here.')
 else:u.is_active=not u.is_active;u.save(update_fields=['is_active']);messages.success(request,'User status updated.')
 return redirect('admin_panel:users')
@staff_member_required
def categories(request):
 form=CategoryForm(request.POST or None)
 if request.method=='POST' and form.is_valid():form.save();messages.success(request,'Category created.');return redirect('admin_panel:categories')
 return render(request,'admin_panel/categories.html',{'categories':Category.objects.all(),'form':form})
@staff_member_required
@require_POST
def delete_category(request,pk):get_object_or_404(Category,pk=pk).delete();messages.success(request,'Category deleted; posts become uncategorized.');return redirect('admin_panel:categories')
@staff_member_required
def comments(request):return render(request,'admin_panel/comments.html',{'comments':Comment.objects.select_related('author','post').order_by('-created_at')})
@staff_member_required
@require_POST
def delete_comment(request,pk):get_object_or_404(Comment,pk=pk).delete();messages.success(request,'Comment deleted.');return redirect('admin_panel:comments')
@staff_member_required
def messages_list(request):return render(request,'admin_panel/messages.html',{'messages_list':ContactMessage.objects.all()})
@staff_member_required
@require_POST
def toggle_message(request,pk):m=get_object_or_404(ContactMessage,pk=pk);m.is_read=not m.is_read;m.save(update_fields=['is_read']);return redirect('admin_panel:messages')
@staff_member_required
@require_POST
def delete_message(request,pk):get_object_or_404(ContactMessage,pk=pk).delete();messages.success(request,'Message deleted.');return redirect('admin_panel:messages')
