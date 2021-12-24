from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import generic
from accounts import forms
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
from django.contrib.auth import authenticate,login

# Create your views here.
class SignUp(generic.CreateView):
    form_class=forms.UserCreateForm
    success_url=reverse_lazy('home')
    template_name='accounts/signup.html'

    def form_valid(self,form):
        subject='Welcome to the NFL Lines Competition!'
        message='Hello ' + form.cleaned_data['username'] + ',\nThank you for registering for the NFL Lines Competition! If you have any questions or concerns, please contact us at nfllinescompetition@gmail.com.\nGood luck picking!\n\nnfllinescompetition.com'
        fromemail=settings.EMAIL_HOST_USER
        toemail=[form.cleaned_data['email']]
        try:
            send_mail(
                subject,
                message,
                fromemail,
                toemail,
                fail_silently=False
            )
            newuser=form.save()
            newuser=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            login(self.request,newuser)
            return redirect('home')
        except BadHeaderError:
            pass