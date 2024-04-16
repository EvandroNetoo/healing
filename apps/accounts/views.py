from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'register.html')
    
    def post(self, request: HttpRequest) -> HttpResponse:
        return redirect()


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        return redirect()


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        return redirect()
