from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('auth:index')
