from django.urls import path
from django.contrib.auth.decorators import login_required

from authentication.views import IndexView, LogoutView


app_name = 'auth'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('logout/', login_required(LogoutView.as_view(), login_url='/'), name='logout')
]
