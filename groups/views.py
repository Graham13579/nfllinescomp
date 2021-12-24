from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404,get_list_or_404
from django.contrib import messages
from groups.models import Group,Player,Game,PlayerPick
from groups.forms import CreateGroupForm,PasswordAttemptForm,UpdateGroupForm,BasePlayerPickForm
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.template import Context
from django import forms
from django.forms import modelformset_factory
from itertools import chain
from django.http import HttpResponseRedirect
from json import dumps
from datetime import datetime,timedelta,date
import random
from django.contrib.auth import get_user_model
from groups.filters import GroupFilter

@login_required
def creategroup(request):
    #Weeks left maker - need to integrate into maximum validator in model
    startdate=date(2021,3,12)
    currentdate=date.today()
    dayspassed=int(str(currentdate-startdate)[0])
    weekspassed=int(dayspassed / 7)
    weeksleft=17-weekspassed
    if request.method == 'POST':
        form=CreateGroupForm(request.POST)
        # User=get_user_model()
        # user=User.objects.get(username=request.user)
        # if form.is_valid() and (form.cleaned_data['paidorfree'] == 'Free' or form.cleaned_data['cost'] <= user.userprofile.creditamount):
        if form.is_valid() and form.cleaned_data['length'] <= weeksleft:
            try:
                form.save()
                group=Group.objects.filter(name=form.cleaned_data['name'])[0]
                # if (datetime.now().today().weekday() > 2 and datetime.now().today().weekday() < 6)and (group.length == 'One Week' and group.ppw > 15):
                #     group.ppw=15
                #     group.save()
                # elif (datetime.now().today().weekday() == 6 and datetime.now().today().weekday()) and group.length == 'One Week':
                    # hoursdelay=24*(15-datetime.now().today().weekday())
                    # group.enddate=datetime.now() + timedelta(hours=hoursdelay)
                    # group.save()
                # else:
                #     pass
                if datetime.now().today().weekday() < 6 and datetime.now().today().weekday() > 0:
                    daydelay=8-datetime.now().today().weekday()
                    end=datetime.now() + timedelta(weeks=group.length-1,days=daydelay)
                    end=end.replace(hour=0, minute=0, second=0, microsecond=0)
                    group.enddate=end
                    group.save()
                else:
                    if datetime.now().today().weekday() == 6:
                        end=datetime.now() + timedelta(weeks=group.length,days=2)
                        end=end.replace(hour=0, minute=0, second=0, microsecond=0)
                        group.enddate=end
                        group.save()
                    if datetime.now().today().weekday() == 0:
                        end=datetime.now() + timedelta(weeks=group.length,days=1)
                        end=end.replace(hour=0, minute=0, second=0, microsecond=0)
                        group.enddate=end
                        group.save()
                return redirect("groups:join",group.slug)
            except IntegrityError:
                messages.add_message(request,messages.INFO,"This group name is already in use")
                return render(request,"groups/group_form.html",{'form':form,'weeksleft':weeksleft})
        else:
            form=CreateGroupForm
            return render(request,"groups/group_form.html",{'form':form,'weeksleft':weeksleft})
    else:
        form=CreateGroupForm
    return render(request,"groups/group_form.html",{'form':form,'weeksleft':weeksleft})

class SingleGroup(LoginRequiredMixin,generic.DetailView):
    model=Group

    def get_context_data(self,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        context=super(SingleGroup,self).get_context_data(**kwargs)
        context['members']=Player.objects.filter(group=group).order_by('-score')
        context['playerpicks']=PlayerPick.objects.filter(player__group=group)
        context['pickingplayer']=(Player.objects.filter(user=self.request.user,group=group))
        return context

@login_required
def makegrouppicks(request,slug):
    group=get_object_or_404(Group,slug=slug)
    members=Player.objects.filter(group=group).order_by('-score')
    pickingplayer=(Player.objects.get(user=request.user,group=group))
    playerpicks=PlayerPick.objects.filter(player__group=group)
    gamelinesdict={}
    for game in Game.objects.all():
        gamelinesdict[game.favorite]="-"+str(game.line)
    gamelinesJSON=dumps(gamelinesdict)
    endearly=False
    if request.method == 'POST':
        creationtime=datetime.now()
        formset=BasePlayerPickForm(request.POST)
        if formset.is_valid():
            formset.save()
            messagecount=0
            for item in formset.cleaned_data:
                for game in Game.objects.all():
                    starttimeobject=datetime.strptime(game.starttime,'%Y-%m-%d %H:%M') + timedelta(hours=0)
                    if (str(starttimeobject.strftime('%Y-%m-%d %H:%M')) > str(datetime.now().strftime('%Y-%m-%d %H:%M'))) and game.pickable == True:
                        try:
                            if game.favorite == item.get('teampicked')[0] or game.underdog == item.get('teampicked')[0]:
                                gamepicked=game
                            try:
                                pickcount=PlayerPick.objects.filter(player=pickingplayer).count()
                            except:
                                pickcount=0
                            if pickcount > group.ppw:
                                if messagecount == 0:
                                    if group.ppw == 1:
                                        messages.warning(request,'You picked too many teams! You can only pick ' + str(group.ppw) + ' game per week in this group!')
                                    else:
                                        messages.warning(request,'You picked too many teams! You can only pick ' + str(group.ppw) + ' games per week in this group!')
                                    messagecount=1
                                endearly=True
                                break
                            ppick=PlayerPick(gamepicked=gamepicked,player=pickingplayer,teampicked=item.get('teampicked')[0],timemade=creationtime)
                            try:
                                ppick.save()
                            except IntegrityError:
                                pass
                        except:
                            pass
            if not endearly:
                return redirect("groups:single",group.slug)
            else:
                for gameday in Game.objects.all():
                    PlayerPick.objects.filter(gamepicked=gameday,timemade=creationtime).delete()
                return HttpResponseRedirect(request.path_info)
    else:
        gamefavoritesinform=[]
        for game in Game.objects.all():
            #watch timedelta
            starttimeobject=datetime.strptime(game.starttime,'%Y-%m-%d %H:%M') + timedelta(hours=0)
            if (str(starttimeobject.strftime('%Y-%m-%d %H:%M')) > str(datetime.now().strftime('%Y-%m-%d %H:%M'))) and game.pickable == True:
                gamefavoritesinform.append(game.favorite)
                print((str(starttimeobject.strftime('%Y-%m-%d %H:%M'))))
                print(str(datetime.now().strftime('%Y-%m-%d %H:%M')))
        formset=BasePlayerPickForm(queryset=Game.objects.filter(favorite__in=gamefavoritesinform))
    return render(request,"groups/group_make_picks.html",{'formset':formset,'group':group,'members':members,'playerpicks':playerpicks,'pickingplayer':pickingplayer,'games':Game.objects.all(),'gamelines':gamelinesJSON})

@login_required
def updategroup(request,slug):
    group=get_object_or_404(Group,slug=slug)
    if request.method == 'POST':
        form = UpdateGroupForm(request.POST,instance=group)
        if form.is_valid():
            try:
                form.save()
                return redirect("groups:single",group.slug)
            except IntegrityError:
                messages.add_message(request,messages.INFO,"This group name is already in use")
                return render(request,"groups/group_update.html",{'form':form,'group':group})
    else:
        form=UpdateGroupForm(instance=group)
    return render(request,"groups/group_update.html",{'form':form,'group':group})

class ListGroups(generic.ListView):
    model=Group

class FindGroups(generic.ListView):
    template_name='groups/group_find.html'
    model=Group

    def get_queryset(self):
        query=self.request.GET.get('name')
        length=self.request.GET.get('length')
        ppw=self.request.GET.get('ppw')
        numplayers=self.request.GET.get('numplayers')
        if query or length or ppw or numplayers:
            group_list=Group.objects.all()
            group_filter=GroupFilter(self.request.GET,queryset=group_list)
            if query and not length and not ppw and not numplayers:
                matching_name=self.model.objects.filter(name=query)
                close_matching_name=self.model.objects.filter(name__icontains=query,active=True)
                object_list=list(set(chain(matching_name,close_matching_name)))
            else:
                object_list=group_filter.qs
        else:
            if self.model.objects.count() > 15:
                object_list=random.sample(list(self.model.objects.all()),15)
            else:
                object_list=self.model.objects.all()
        return object_list

class PlayerCapReached(LoginRequiredMixin,generic.ListView):
    template_name='groups/group_playercap.html'
    model=Group

    def get_context_data(self,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        context = super(PlayerCapReached,self).get_context_data(**kwargs)
        context['group_name'] = group.name
        return context

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        if group.privacy == 'Private' and group.owner != self.request.user:
            group.passwordattempt='a'
            group.save()
            return reverse('groups:password',kwargs={'slug':self.kwargs.get('slug')})
        else:
            if group.members.count() != group.numplayers:
                return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
            else:
                return reverse('groups:playercap',kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        if group.privacy == 'Public' or group.members.count() == 0:
            if group.members.count() != group.numplayers:
                try:
                    if group.members.count() == 0:
                        group.owner=self.request.user
                        group.save()
                    Player.objects.create(user=self.request.user,group=group)
                    # if group.paidorfree == 'Paid':
                    #     User=get_user_model()
                    #     user=User.objects.get(username=request.user)
                    #     currentpaymentamount=group.cost
                    #     currentcreditamount=user.userprofile.creditamount
                    #     user.userprofile.creditamount=currentcreditamount-currentpaymentamount
                    #     user.userprofile.save()
                    #     currentpotamount=group.pot
                    #     group.pot=currentpaymentamount+currentpotamount
                    #     group.save()
                except:
                    # if group.paidorfree == 'Paid':
                    #     user.userprofile.creditamount=currentcreditamount
                    #     user.userprofile.save()
                    #     group.pot=currentpotamount
                    #     group.save()
                    pass
        
                return super().get(request,*args,**kwargs)
        
        return super().get(request,*args,**kwargs)

@login_required
def passwordgroup(request,slug):
    group=get_object_or_404(Group,slug=slug)
    details="groups/password_group.html"
    group.passwordattempt='a'
    group.save()
    if request.method == 'POST':
        form=PasswordAttemptForm(request.POST)
        if group.members.count() != group.numplayers:
            if form.is_valid():
                passwordattempt=form.cleaned_data['passwordattempt']
                group.passwordattempt=passwordattempt
                group.save()
                if group.check_group_password():
                    return redirect('groups:passwordredirect',slug)
        else:
            return redirect('groups:playercap',slug)
    else:
        form = PasswordAttemptForm()
    
    context = {
        'group':get_object_or_404(Group,slug=slug),
        'form':form
    }
    return render(request,details,context)

class PasswordRedirect(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        if group.members.count() != 0:
            if group.privacy == 'Private' and group.check_group_password():
                try:
                    Player.objects.create(user=self.request.user,group=group)
                    # if group.paidorfree == 'Paid':
                    #     User=get_user_model()
                    #     user=User.objects.get(username=request.user)
                    #     currentpaymentamount=group.cost
                    #     currentcreditamount=user.userprofile.creditamount
                    #     user.userprofile.creditamount=currentcreditamount-currentpaymentamount
                    #     user.userprofile.save()
                    #     currentpotamount=group.pot
                    #     group.pot=currentpaymentamount+currentpotamount
                    group.passwordattempt='a'
                    group.save()
                except:
                    # if group.paidorfree == 'Paid':
                    #     user.userprofile.creditamount=currentcreditamount
                    #     user.userprofile.save()
                    #     group.pot=currentpotamount
                    group.passwordattempt='a'
                    group.save()
            
                return super().get(request,*args,**kwargs)
            else:
                return super().get(request,*args,**kwargs)
        else:
            try:
                Player.objects.create(user=self.request.user,group=group)
                group.passwordattempt='a'
                group.save()
            except IntegrityError:
                group.passwordattempt='a'
                group.save()
            else:
                group.passwordattempt='a'
                group.save()
            
            return super().get(request,*args,**kwargs)

@login_required
def leavegroupconfirm(request,slug):
    group=get_object_or_404(Group,slug=slug)
    return render(request,'groups/leave_group_confirm.html',{'group':group})

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('home')
    
    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        if group.owner == request.user:
            if group.members.count() > 2:
                group.owner=(Player.objects.filter(group=group))[0].user
            else:
                # User=get_user_model()
                # user=User.objects.get(username=request.user)
                # currentcreditamount=user.userprofile.creditamount
                # currentrefundamount=group.cost
                # user.userprofile.creditamount=currentcreditamount+currentrefundamount
                # user.userprofile.save()
                pass
                try:
                    membership=Player.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug')).get()
                except Player.DoesNotExist:
                    pass
                else:
                    membership.delete()
                if group.members.count() == 1:
                    playertoberemoved=Player.objects.get(group=group)
                    # currentcreditamount=playertoberemoved.user.userprofile.creditamount
                    # currentrefundamount=group.cost
                    # playertoberemoved.user.userprofile.creditamount=currentcreditamount+currentrefundamount
                    # playertoberemoved.user.userprofile.save()
                    playertoberemoved.delete()
                group.delete()
        else:
            try:
                membership=Player.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug')).get()
            except Player.DoesNotExist:
                pass
            else:
                membership.delete()
            try:
                group.passwordattempt='a'
                group.save()
            except:
                pass
        return super().get(request,*args,**kwargs)