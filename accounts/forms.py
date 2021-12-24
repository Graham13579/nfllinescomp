from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        fields=('username','email','password1','password2')
        model=get_user_model()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # self.fields['username'.label='Display Name']
    
    def clean(self):
        data=self.cleaned_data
        email=self.cleaned_data.get('email')
        username=self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('This email address is already in use.')
        return data