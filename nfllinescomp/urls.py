"""nfllinescomp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from nfllinescomp import views

urlpatterns = [
    path('',views.HomePage.as_view(),name='home'),
    path('makepicks',views.makepicks,name='makepicks'),
    # path('paymentoptions',views.paymentoptions,name='paymentoptions'),
    # path('paypal/pay/<pk>/',views.payment,name='payment'),
    # path('paypal/create/<id>/',views.create,name="paypal-create"),
    # path('paypal/<order_id>/capture/<id>/',views.capture,name="paypal-capture"),
    # path('paypal/client-id/',views.getClientId,name="client-id"),
    # path('withdraw',views.withdraw,name='withdraw'),
    # path('withdrawinbetween',views.withdraw_in_between,name='withdrawinbetween'),
    # path('withdrawsuccess',views.withdrawsuccess,name='withdrawsuccess'),
    # path('withdrawfailure',views.withdrawfailure,name='withdrawfailure'),
    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('groups/',include('groups.urls',namespace='groups')),
    path('admin/', admin.site.urls),
]