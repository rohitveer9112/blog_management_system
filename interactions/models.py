from django.db import models
from django.contrib.auth.models import User
from blogs.models import BlogPost
class Comment(models.Model):
 post=models.ForeignKey(BlogPost,on_delete=models.CASCADE,related_name='comments')
 author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
 body=models.TextField(max_length=2000)
 created_at=models.DateTimeField(auto_now_add=True)
 is_approved=models.BooleanField(default=True)
 class Meta:
  ordering=['created_at']
 def __str__(self):return f'Comment by {self.author}'
class Like(models.Model):
 user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
 post=models.ForeignKey(BlogPost,on_delete=models.CASCADE,related_name='likes')
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:
  constraints=[models.UniqueConstraint(fields=['user','post'],name='unique_user_post_like')]
