from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):
    context = {
        'page': 'dashboard'
    }
    return render(request, 'dashboard/dashboard.html', context)