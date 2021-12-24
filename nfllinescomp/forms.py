from django import forms

class WithdrawForm(forms.Form):
    email=forms.EmailField()
    withdrawlamount=forms.IntegerField(max_value=100)

    def __init__(self, *args, **kwargs):
        super(WithdrawForm,self).__init__(*args,**kwargs)
        self.fields['withdrawlamount'].label="Withdrawl Amount"