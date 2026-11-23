from django import forms
from .models import BlogPost,Category
from PIL import Image, UnidentifiedImageError
class BlogForm(forms.ModelForm):
 action=forms.CharField(widget=forms.HiddenInput(),initial='draft',required=False)
 class Meta:model=BlogPost;fields=['title','content','category','featured_image'];widgets={'content':forms.Textarea(attrs={'rows':12})}
 def clean_featured_image(self):
  f=self.cleaned_data.get('featured_image')
  if f:
   if f.size>5*1024*1024:raise forms.ValidationError('Image must be 5 MB or smaller.')
   try:
    image=Image.open(f); image.verify()
    if image.format not in ['JPEG','PNG','WEBP']:raise forms.ValidationError('Upload a JPG, PNG, or WebP image.')
   except (UnidentifiedImageError,OSError):raise forms.ValidationError('The uploaded file is not a valid image.')
   f.seek(0)
  return f
class CategoryForm(forms.ModelForm):
 class Meta:model=Category;fields=['name','description']
