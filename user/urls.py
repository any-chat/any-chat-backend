from django.urls import path
from user import views as user


urlpatterns = [
    path('login', user.LoginView.as_view(), name='user_login'),
]
