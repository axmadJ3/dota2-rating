from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import IndexView, LogoutView
from rating.views import rating_dashboard_view

app_name = 'auth'

urlpatterns = [
    path('', rating_dashboard_view, name='index'),
    path('logout/', login_required(LogoutView.as_view(), login_url='/'), name='logout')
]
