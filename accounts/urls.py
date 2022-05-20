from django.urls import path

from accounts.views import MyLoginView, MySignupView, MyLogoutView


app_name = 'accounts'

urlpatterns = [
    path('signup/', MySignupView.as_view(), name='signup'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
]
