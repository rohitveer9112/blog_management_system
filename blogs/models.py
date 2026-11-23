from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
class Category(models.Model):
 name=models.CharField(max_length=80,unique=True)
 slug=models.SlugField(unique=True,blank=True)
 description=models.TextField(blank=True)
 def save(self,*a,**kw):
  if not self.slug:self.slug=slugify(self.name)
  super().save(*a,**kw)
 def __str__(self):return self.name
class BlogPost(models.Model):
 class Status(models.TextChoices):
  DRAFT='draft','Draft'
  PENDING='pending','Pending'
  PUBLISHED='published','Published'
  REJECTED='rejected','Rejected'
 title=models.CharField(max_length=180)
 slug=models.SlugField(unique=True,blank=True)
 content=models.TextField()
 featured_image=models.ImageField(upload_to='blog_images/',blank=True)
 author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
 category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='posts')
 status=models.CharField(max_length=12,choices=Status.choices,default=Status.DRAFT,db_index=True)
 rejection_reason=models.TextField(blank=True)
 created_at=models.DateTimeField(auto_now_add=True)
 updated_at=models.DateTimeField(auto_now=True)
 published_at=models.DateTimeField(null=True,blank=True)
 class Meta:
  ordering=['-published_at','-created_at']
  indexes=[models.Index(fields=['status','-published_at'])]
 def save(self,*a,**kw):
  if not self.slug:
   base=slugify(self.title)[:180] or 'post';candidate=base;n=2
   while BlogPost.objects.filter(slug=candidate).exclude(pk=self.pk).exists():candidate=f'{base}-{n}';n+=1
   self.slug=candidate
  if self.status==self.Status.PUBLISHED and not self.published_at:self.published_at=timezone.now()
  super().save(*a,**kw)
 def __str__(self):return self.title
