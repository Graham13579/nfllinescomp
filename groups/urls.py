from django.urls import path
from groups import views

app_name='groups'

urlpatterns=[
    path('',views.ListGroups.as_view(),name='mygroups'),
    # path('new/',views.CreateGroup.as_view(),name='create'),
    path('new/',views.creategroup,name='create'),
    path('update/<slug>/',views.updategroup,name='update'),
    path('find/',views.FindGroups.as_view(),name='find'),
    path('group/<slug>/',views.SingleGroup.as_view(),name='single'),
    path('makepicks/<slug>',views.makegrouppicks,name='makepicks'),
    path('join/<slug>/',views.JoinGroup.as_view(),name='join'),
    path('password/<slug>/',views.passwordgroup,name='password'),
    path('password/join/<slug>/',views.PasswordRedirect.as_view(),name='passwordredirect'),
    path('playercapreachednotification/<slug>',views.PlayerCapReached.as_view(),name='playercap'),
    path('leave/confirm/<slug>',views.leavegroupconfirm,name='leaveconfirm'),
    path('leave/<slug>/',views.LeaveGroup.as_view(),name='leave'),
]