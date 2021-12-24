from django.views import generic
from groups.models import Group,Player,Game,PlayerPick
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect,get_object_or_404
from json import dumps
from groups.forms import BasePlayerPickForm
from django.db import IntegrityError
from datetime import datetime,timedelta
# from django.conf import settings
# from accounts.models import CreditPaymentPackage,Payment,UserProfile
# from django.http import JsonResponse
# from paypalcheckoutsdk.orders import OrdersCreateRequest,OrdersCaptureRequest
# from paypalcheckoutsdk.core import SandboxEnvironment,PayPalHttpClient
# from django.contrib.auth.decorators import login_required
# from paypalpayoutssdk.payouts import PayoutsPostRequest,PayoutsGetRequest
# import random
# from nfllinescomp.forms import WithdrawForm

class HomePage(generic.ListView):
    template_name='index.html'
    model=Group

def makepicks(request):
    user=request.user
    usergroups=Group.objects.filter(members=user)
    for usergroup in usergroups:
        tempplayer=Player.objects.get(group=usergroup,user=user)
        if tempplayer.picks.count() > 0:
            usergroups=usergroups.exclude(name=usergroup.name)
    gamelinesdict={}
    for game in Game.objects.all():
        gamelinesdict[game.favorite]="-"+str(game.line)
    gamelinesJSON=dumps(gamelinesdict)
    if request.method == 'POST':
        creationtime=datetime.now()
        formset=BasePlayerPickForm(request.POST)
        if formset.is_valid():
            formset.save()
            groupschosenkeys=[]
            groupschosen=[]
            for key in request.POST.keys():
                if "groupcheckboxresult" in key:
                    groupschosenkeys.append(key)
            for key in groupschosenkeys:
                groupschosen.append(request.POST[key])
            for chosengroup in groupschosen:
                for usergroup in usergroups:
                    if usergroup.name == chosengroup:
                        finalgroupchosenname=usergroup.name
                        break
                finalgroupchosen=Group.objects.filter(name=finalgroupchosenname)[0]
                groupuserplayer=Player.objects.filter(group=finalgroupchosen,user=user)[0]
                count=len(PlayerPick.objects.filter(player=groupuserplayer))
                for item in formset.cleaned_data:
                    for game in Game.objects.all():
                        try:
                            starttimeobject=datetime.strptime(game.starttime,'%Y-%m-%d %H:%M') + timedelta(hours=0)
                            if (str(starttimeobject.strftime('%Y-%m-%d %H:%M')) > str(datetime.now().strftime('%Y-%m-%d %H:%M'))) and game.pickable == True:
                                if game.favorite == item.get('teampicked')[0] or game.underdog == item.get('teampicked')[0]:
                                    count+=1
                                    gamepicked=game
                            else:
                                continue
                            if count > finalgroupchosen.ppw:
                                break
                            ppick=PlayerPick(gamepicked=gamepicked,player=groupuserplayer,teampicked=item.get('teampicked')[0],timemade=creationtime)
                            try:
                                ppick.save()
                            except IntegrityError:
                                pass
                        except:
                            pass
            return redirect('home')
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
    return render(request,'make_picks.html',{'formset':formset,'usergroups':usergroups,'gamelines':gamelinesJSON})

# @login_required
# def paymentoptions(request):
#     creditpaymentpackages=CreditPaymentPackage.objects.all()
#     return render(request,'payment_options.html',{'creditpaymentpackages':creditpaymentpackages})

# @login_required
# def payment(request,pk):
#     client_id=settings.PAYPAL_CLIENT_ID
#     creditpaymentpackage=get_object_or_404(CreditPaymentPackage,pk=pk)
#     return render(request,'payment.html',{'creditpaymentpackage':creditpaymentpackage,'client_id':client_id })

# @login_required
# def create(request,id):
#     if request.method=="POST":
#         environment=SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_ID)
#         client=PayPalHttpClient(environment)

#         creditpaymentpackage=CreditPaymentPackage.objects.get(pk=id)
#         create_order=OrdersCreateRequest()

#         create_order.request_body (
#             {
#                 "intent": "CAPTURE",
#                 "purchase_units": [
#                     {
#                         "amount": {
#                             "currency_code": "USD",
#                             "value": creditpaymentpackage.price,
#                             "breakdown": {
#                                 "item_total": {
#                                     "currency_code": "USD",
#                                     "value": creditpaymentpackage.price
#                                 }
#                             },
#                         },
#                     }
#                 ],
#                 "application_context": {
#                     "shipping_preference":"NO_SHIPPING"
#                 }
#             }
#         )

#         response = client.execute(create_order)
#         data = response.result.__dict__['_dict']
#         return JsonResponse(data)
#     else:
#         return JsonResponse({'details':"invalid request"})

# @login_required
# def capture(request,order_id,id):
#     if request.method =="POST":
#         capture_order=OrdersCaptureRequest(order_id)
#         environment=SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID,client_secret=settings.PAYPAL_SECRET_ID)
#         client=PayPalHttpClient(environment)

#         response=client.execute(capture_order)
#         data=response.result.__dict__['_dict']
#         try:
#             User=get_user_model()
#             user=User.objects.get(username=request.user)
#             currentpaymentamount=float(data['purchase_units'][0]['payments']['captures'][0]['amount']['value'])
#             currentcreditamount=user.userprofile.creditamount
#             user.userprofile.creditamount=currentpaymentamount+currentcreditamount
#             user.userprofile.save()
#             return JsonResponse(data)
#         except:
#             user.userprofile.creditamount=currentcreditamount
#             user.userprofile.save()
#             return JsonResponse({'details':"invalid request"})
#     else:
#         return JsonResponse({'details':"invalid request"})

# @login_required
# def getClientId(request):
#     if request.method=="GET":
#         return JsonResponse({'client_id':settings.PAYPAL_CLIENT_ID})

# def withdraw(request):
#     form=WithdrawForm
#     return render(request,'withdraw.html',{'form':form})

# def withdraw_in_between(request):
#     form=WithdrawForm(request.POST)
#     if form.is_valid():
#         User=get_user_model()
#         user=User.objects.get(username=request.user)
#         currentcreditamount=user.userprofile.creditamount
#         paypalemail=form.cleaned_data["email"]
#         withdrawlamount=form.cleaned_data["withdrawlamount"]
#         if (withdrawlamount <= currentcreditamount and withdrawlamount >= 1) and withdrawlamount % 1 == 0:
#             try:
#                 # Construct a request object and set desired parameters
#                 # Here, PayoutsPostRequest()() creates a POST request to /v1/payments/payouts
#                 environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_ID)
#                 client = PayPalHttpClient(environment)
#                 try:
#                     senderbatchid=str(random.randint(100000000,999999999999999))
#                     body = {
#                         "sender_batch_header": {
#                             "recipient_type": "EMAIL",
#                             "email_message": "SDK payouts test txn",
#                             "note": "Enjoy your Payout!!",
#                             "sender_batch_id": senderbatchid,
#                             "email_subject": "This is a test transaction from SDK"
#                         },
#                         "items": [{
#                             "note": "Your " + str(withdrawlamount) + "$ Payout!",
#                             "amount": {
#                                 "currency": "USD",
#                                 "value": str(withdrawlamount)
#                             },
#                             "receiver": paypalemail,
#                             "sender_item_id": "Test_txn_3"
#                         }]
#                     }

#                     payoutrequest = PayoutsPostRequest()
#                     payoutrequest.request_body (body)

#                     # Call API with your client and get a response for your call
#                     response = client.execute(payoutrequest)
#                     # If call returns body in response, you can get the deserialized version from the result attribute of the response
#                     batch_id = response.result.batch_header.payout_batch_id

#                     payoutrequest = PayoutsGetRequest(batch_id)

#                     # Call API with your client and get a response for your call
#                     response = client.execute(payoutrequest)

#                     # If call returns body in response, you can get the deserialized version from the result attribute of the response
#                     batch_status = response.result.batch_header.batch_status

#                     currentcreditamount=user.userprofile.creditamount
#                     user.userprofile.creditamount=currentcreditamount-withdrawlamount
#                     user.userprofile.save()
#                     return redirect('withdrawsuccess')
#                 except:
#                     senderbatchid=str(random.randint(100000000,999999999999999))
#                     body = {
#                         "sender_batch_header": {
#                             "recipient_type": "EMAIL",
#                             "email_message": "SDK payouts test txn",
#                             "note": "Enjoy your Payout!!",
#                             "sender_batch_id": senderbatchid,
#                             "email_subject": "This is a test transaction from SDK"
#                         },
#                         "items": [{
#                             "note": "Your " + str(withdrawlamount) + "$ Payout!",
#                             "amount": {
#                                 "currency": "USD",
#                                 "value": str(withdrawlamount)
#                             },
#                             "receiver": paypalemail,
#                             "sender_item_id": "Test_txn_3"
#                         }]
#                     }

#                     payoutrequest = PayoutsPostRequest()
#                     payoutrequest.request_body (body)

#                     # Call API with your client and get a response for your call
#                     response = client.execute(payoutrequest)
#                     # If call returns body in response, you can get the deserialized version from the result attribute of the response
#                     batch_id = response.result.batch_header.payout_batch_id

#                     payoutrequest = PayoutsGetRequest(batch_id)

#                     # Call API with your client and get a response for your call
#                     response = client.execute(payoutrequest)

#                     # If call returns body in response, you can get the deserialized version from the result attribute of the response
#                     batch_status = response.result.batch_header.batch_status

#                     currentcreditamount=user.userprofile.creditamount
#                     user.userprofile.creditamount=currentcreditamount-withdrawlamount
#                     user.userprofile.save()
#                     return redirect('withdrawsuccess')
#             except:
#                 try:
#                     user.userprofile.creditamount=currentcreditamount
#                     user.userprofile.save()
#                 except:
#                     pass
#                 return redirect('withdrawfailure')
#         else:
#             return redirect('withdrawfailure')
#     else:
#         return redirect('withdrawfailure')


# def withdrawsuccess(request):
#     return render(request,'withdraw_success.html')

# def withdrawfailure(request):
#     return render(request,'withdraw_failure.html')