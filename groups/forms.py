from django import forms
from groups.models import Group,PlayerPick,Game
from django.forms import modelformset_factory

class CreateGroupForm(forms.ModelForm):
    password=forms.CharField(label="Group Password",widget=forms.PasswordInput)
    class Meta:
        model=Group
        # fields=('name','privacy','password','paidorfree','cost','length','ppw','numplayers','description')
        fields=('name','privacy','password','length','ppw','numplayers','description')
    
    PRIVACY_CHOICES=[('Public','Public'),('Private','Private')]
    privacy=forms.ChoiceField(label="Do you want a public or password protected group?",choices=PRIVACY_CHOICES,widget=forms.RadioSelect)
    
    # LENGTH_CHOICES=[('One Week','One Week'),('Season-long','Season-long')]
    # length=forms.ChoiceField(choices=LENGTH_CHOICES,widget=forms.RadioSelect)
    
    # PPW_CHOICES=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16)]
    # ppw=forms.ChoiceField(label="Picks per week",choices=PPW_CHOICES,widget=forms.RadioSelect)

    # NUMPLAYERS_CHOICES=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19,19),(20,20),(21,21),(22,22),(23,23),(24,24),(25,25)]
    # numplayers=forms.ChoiceField(label="Max number of players",choices=NUMPLAYERS_CHOICES,widget=forms.RadioSelect)

class PasswordAttemptForm(forms.ModelForm):
    class Meta:
        model=Group
        fields=('passwordattempt',)

    passwordattempt=forms.CharField(label='Password:',max_length=20,widget=forms.PasswordInput())

class UpdateGroupForm(forms.ModelForm):
    password=forms.CharField(label="Group Password",widget=forms.PasswordInput)
    class Meta:
        model=Group
        fields=('name','privacy','password', 'description')
    
    name=forms.CharField(label='New Group Name:',max_length=256)

    PRIVACY_CHOICES=[('Public','Public'),('Private','Private')]
    privacy=forms.ChoiceField(label="Do you want a public or password protected group?",choices=PRIVACY_CHOICES,widget=forms.RadioSelect)

class MakePlayerPickForm(forms.ModelForm):
    class Meta:
        model=Game
        fields=('teampicked',)
    
    def __init__(self,*args,**kwargs):
        super(MakePlayerPickForm,self).__init__(*args,**kwargs)
        namelist=str(kwargs['instance']).split(" vs ")
        self.fields['teampicked']=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[(namelist[0],namelist[0]),(namelist[1],namelist[1])])
        self.fields['teampicked'].required=False

BasePlayerPickForm=modelformset_factory(model=Game,form=MakePlayerPickForm,extra=0)