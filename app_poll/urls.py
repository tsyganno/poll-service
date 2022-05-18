from django.urls import path
from app_poll.views import IndexView


app_name = 'poll'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
