from django.contrib import messages
from django.shortcuts import render,redirect
from .forms import ContactForm
def contact(request):
 form=ContactForm(request.POST or None)
 if request.method=='POST' and form.is_valid():form.save();messages.success(request,'Thanks. Your message has been sent.');return redirect('contact:form')
 return render(request,'contact/form.html',{'form':form})
