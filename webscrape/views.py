from django.shortcuts import render, redirect
from lead.models import HKTDCRequest
from django.contrib.auth.decorators import login_required
import csv

# Create your views here.
@login_required
def hktdc_tasks(request):
    context = {
        'requests': HKTDCRequest.objects.all(),
        'page': 'hktdc_task'
    }
    return render(request, "lead/hktdc_tasks.html", context)


@login_required
def hktdc_tasks_result(request, id):
    hktdc_request = HKTDCRequest.objects.filter(id = id).first()
    if not hktdc_request:
        return redirect("dashboard")
    
    csv_data = hktdc_request.read_csv_file()
    for row in csv_data:
        print(row)
    
    context = {
        'hktdc_request': hktdc_request,
        'requests': HKTDCRequest.objects.all(),
        'page': 'hktdc_task',
        'csv_data': csv_data
    }
    return render(request, "lead/hktdc_tasks_result.html", context)