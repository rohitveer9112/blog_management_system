from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from PIL import Image, UnidentifiedImageError
class RegisterForm(UserCreationForm):
 email=forms.EmailField(required=True)
 class Meta(UserCreationForm.Meta):
  model=User
  fields=('username','email','password1','password2')
 def save(self,commit=True):
  user=super().save(commit=False);user.email=self.cleaned_data['email']
  if commit:user.save()
  return user
class ProfileForm(forms.ModelForm):
 class Meta:
  model=UserProfile
  fields=['bio','photo','website']
 def clean_photo(self):
  f=self.cleaned_data.get('photo')
  if f:
   if f.size>3*1024*1024:raise forms.ValidationError('Image must be 3 MB or smaller.')
   try:
    image=Image.open(f);image.verify()
    if image.format not in ['JPEG','PNG','WEBP']:raise forms.ValidationError('Upload a JPG, PNG, or WebP image.')
   except (UnidentifiedImageError,OSError):raise forms.ValidationError('The uploaded file is not a valid image.')
   f.seek(0)
  return f
class UserDetailsForm(forms.ModelForm):
 class Meta:
  model=User
  fields=['first_name','last_name','email']
