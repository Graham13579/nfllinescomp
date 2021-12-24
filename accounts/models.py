from django.db import models
from django.contrib import auth
# from django.core.validators import MinValueValidator,MaxValueValidator
# from annoying.fields import AutoOneToOneField

# Create your models here.
class User(auth.models.User,auth.models.PermissionsMixin):
    def __str__(self):
        return self.username

# class UserProfile(models.Model):
#     user=AutoOneToOneField(auth.models.User,on_delete=models.CASCADE,primary_key=True)
#     creditamount=models.FloatField(default=0,validators=[MinValueValidator(0), MaxValueValidator(1000)])

#     def __str__(self):
#         return self.user.username

# class CreditPaymentPackage(models.Model):
#     name=models.CharField(max_length=20)
#     price=models.FloatField()

# class Payment(models.Model):
#     creditpaymentpackage=models.ForeignKey(CreditPaymentPackage,on_delete=models.CASCADE)