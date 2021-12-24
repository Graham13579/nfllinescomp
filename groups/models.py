from django.db import models
from django.utils.text import slugify
import misaka
from django.contrib.auth import get_user_model
from django import template
from django.urls import reverse
from django.core.validators import MinValueValidator,MaxValueValidator
from django import forms
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
from datetime import datetime,timedelta

# Create your models here.
User=get_user_model()

register=template.Library()

class Group(models.Model):
    name=models.CharField("Group Name",max_length=256,unique=True)
    PUBLIC='Public'
    PRIVATE='Private'
    PRIVACY_CHOICES=[(PUBLIC,'Public'),(PRIVATE,'Private')]
    privacy=models.CharField("Do you want a public or password protected group?",max_length=20,choices=PRIVACY_CHOICES,default=PUBLIC)
    # PAID='Paid'
    # FREE='Free'
    # PAID_FREE_CHOICES=[(PAID,'Paid'),(FREE,'Free')]
    # paidorfree=models.CharField('Free or Paid',max_length=7,choices=PAID_FREE_CHOICES,default=FREE)
    # cost=models.IntegerField('Cost of Entry',validators=[MinValueValidator(5),MaxValueValidator(50)])
    password=models.CharField("Group Password",max_length=20,default='')
    passwordattempt=models.CharField(max_length=20,default='a')
    # ONE_WEEK='One Week'
    # SEASON='Season-long'
    # LENGTH_CHOICES=[(ONE_WEEK,'One Week'),(SEASON,'Season-long')]
    # length=models.CharField(max_length=11,choices=LENGTH_CHOICES,default=ONE_WEEK)
    ###
    ### NEEDS TO CHANGE TO BE DYNAMIC ###
    ###
    length=models.IntegerField("How many weeks will your group run for? (1-" + str(17) + ")",validators=[MinValueValidator(1), MaxValueValidator(17)])
    startdate=models.CharField("Group start date",default=datetime.now().strftime('%Y-%m-%d %H:%M'),max_length=30)
    startdaydate=models.CharField(default=datetime.now().strftime('%A'),max_length=20)
    enddate=models.CharField(default='',max_length=30)
    active=models.BooleanField(default=True)
    # PPW_CHOICES=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16)]
    # ppw=models.IntegerField("Number of Picks Per Week",choices=PPW_CHOICES,validators=[MinValueValidator(1), MaxValueValidator(16)])
    ppw=models.IntegerField("How many games will people in your group pick every week? (1-16)",validators=[MinValueValidator(1), MaxValueValidator(16)])
    # NUMPLAYERS_CHOICES=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19,19),(20,20),(21,21),(22,22),(23,23),(24,24),(25,25)]
    # numplayers=models.IntegerField("Max number of players",choices=NUMPLAYERS_CHOICES,validators=[MinValueValidator(1), MaxValueValidator(25)])
    numplayers=models.IntegerField("What is the maximum number of people who can be in your group? (25 max)",validators=[MinValueValidator(1), MaxValueValidator(25)])
    description=models.TextField("Group Description (optional)",default='',blank=True)
    members=models.ManyToManyField(User,through='Player')
    # pot=models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(125)])
    winner=models.CharField(default='',max_length=100000)
    owner=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='group_owner',null=True)
    slug=models.SlugField(default='',allow_unicode=True,unique=True)

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        if len(self.password) < 20:
            self.password=make_password(self.password)
        # Needs more work *** Important! :D
        if str(self.enddate) < str(datetime.now().strftime('%Y-%m-%d %H:%M')):
            highscore=-1000
            self.active=False
            for player in Player.objects.filter(group=self):
                if player.score > highscore:
                    highscore=player.score
            try:
                winnerlist=[]
                winners=Player.objects.filter(group=self,score=highscore)
                for winner in winners:
                    winnerlist.append(str(winner))
                if len(winnerlist) > 0:
                    # if self.paidorfree == 'Paid':
                    #     creditwinningsperwinner=(self.pot / len(winnerlist)) - 0.004999
                    #     creditwinningsperwinner=round(creditwinningsperwinner,2)
                    # else:
                        # creditwinningsperwinner=0
                    self.winner=''
                    for winningplayer in winnerlist:
                        # if self.paidorfree == 'Paid':
                        #     try:
                        #         User=get_user_model()
                        #         user=User.objects.get(username=winningplayer)
                        #         currentcreditamount=user.userprofile.creditamount
                        #         user.userprofile.creditamount=creditwinningsperwinner+currentcreditamount
                        #         user.userprofile.save()
                        #     except:
                        #         user.userprofile.creditamount=currentcreditamount
                        #         user.userprofile.save()
                        self.winner=self.winner+winningplayer+'^'
            except:
                pass
        super(Group,self).save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})
    
    def check_group_password(self):
        return check_password(self.passwordattempt,self.password)
    
    class Meta:
        ordering=['name']

class Game(models.Model):
    favorite=models.CharField(max_length=50,blank=True,default='')
    underdog=models.CharField(max_length=50,blank=True,default='')
    line=models.FloatField(blank=True,default=0.0)
    gamedate=models.CharField(default=timezone.now().today().strftime('%A'),max_length=20)
    winner=models.CharField(max_length=50,blank=True,default='')
    winnerscore=models.IntegerField(blank=True,default=0)
    loserscore=models.IntegerField(blank=True,default=0)
    scoredifferential=models.IntegerField(blank=True,default=0)
    teampicked=models.CharField(max_length=50,blank=True,default='')
    pickable=models.BooleanField(default=True)
    starttime=models.CharField(max_length=30,default='')
    
    def __str__(self):
        return self.favorite+' vs '+self.underdog
    
    def save(self,*args,**kwargs):
        if self.winner != '':
            self.pickable = False
        super(Game,self).save(*args,**kwargs)

class Player(models.Model):
    group=models.ForeignKey(Group,related_name='memberships',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)
    score=models.IntegerField(default=0,validators=[MinValueValidator(0)])
    picks=models.ManyToManyField(Game,through='PlayerPick')

    def __str__(self):
        return self.user.username
    
    def add_weekly_score(self):
        self.picks.PlayerPick.score_to_add()
    
    class Meta:
        unique_together=('group','user')
        ordering=['score']

class PlayerPick(models.Model):
    gamepicked=models.ForeignKey(Game,related_name='games_picked',on_delete=models.CASCADE)
    player=models.ForeignKey(Player,related_name='playerchoosing',on_delete=models.CASCADE)
    teampicked=models.CharField(max_length=50,default='')
    timemade=models.CharField(max_length=30,default='')

    def score_to_add(self):
        if self.teampicked != '' or self.gamepicked.favorite+self.gamepicked.underdog:
            if self.gamepicked.scoredifferential == 0 and self.gamepicked.line == 0:
                return 0.5
            if self.gamepicked.scoredifferential == 0:
                if self.teampicked == self.gamepicked.underdog:
                    return 1
                else:
                    return 0
            if self.gamepicked.winner == self.gamepicked.favorite:
                if self.gamepicked.scoredifferential > self.gamepicked.line:
                    if self.teampicked == self.gamepicked.favorite:
                        return 1
                    else:
                        return 0
                if self.gamepicked.line > self.gamepicked.scoredifferential:
                    if self.teampicked == self.gamepicked.underdog:
                        return 1
                    else:
                        return 0
                else:
                    return 0.5
            else:
                if self.teampicked == self.gamepicked.underdog:
                    return 1
                else:
                    return 0
        else:
            return 0

    def __str__(self):
        return self.player.user.username+': '+self.gamepicked.favorite+' vs '+self.gamepicked.underdog

    class Meta:
        unique_together=('gamepicked','player')