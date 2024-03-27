from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from .models import UserProfile
from django.views import View

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            # Save the new user object
            userprofile = UserProfile.objects.create(user=user)
            form.save()
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'userprofile/signup.html', {'form': form})

def login(request):
    return render(request, 'userprofile/login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')  # assuming 'index' is the name of your home url
