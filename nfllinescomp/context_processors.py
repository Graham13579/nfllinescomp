# from accounts.models import UserProfile
# from django.contrib.auth import get_user_model
# def add_creditamount_to_context(request):
#     try:
#         User=get_user_model()
#         user=User.objects.get(username=request.user)
#         if user.userprofile.creditamount % 1 == 0:
#             return{
#                 'withdrawcreditamount':int(user.userprofile.creditamount)
#             }
#         else:
#             if len(str(round(user.userprofile.creditamount % 1,2))) == 4:
#                 return{
#                     'withdrawcreditamount':user.userprofile.creditamount
#                 }
#             else:
#                 return{
#                     'withdrawcreditamount':str(user.userprofile.creditamount) + '0'
#                 }
#     except:
#         return{
#             'withdrawcreditamount':0
#         }