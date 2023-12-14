from django.urls import path

from core import views


app_name = 'core'

urlpatterns = [
    path('auth', views.CreateTokenView.as_view(), name='auth'),
    path('profile', views.ManageUserAccountView.as_view(), name='profile'),
]
