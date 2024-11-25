from django.shortcuts import render

# Create your views here.
def ilogin(request):
    return render(request, 'user/login.html')