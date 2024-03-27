from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .forms import AddLeadForm, WebScrapingForm
from .models import Lead
from django.utils import timezone
from django.core.paginator import Paginator

@login_required
def add_lead(request):
    return render(request, 'lead/add_lead.html')




@login_required
def leads_list(request):
    lead_list = Lead.objects.all()  # Get all leads
    paginator = Paginator(lead_list, 15)  # Show 5 leads per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Generate the range of page numbers
    page_range = range(1, page_obj.paginator.num_pages + 1)

    # Get previous and next page numbers
    previous_page_number = page_obj.previous_page_number() if page_obj.has_previous() else None
    next_page_number = page_obj.next_page_number() if page_obj.has_next() else None

    return render(request, 'lead/lead_list.html', {
        'leads': page_obj,
        'page_range': page_range,
        'previous_page_number': previous_page_number,
        'next_page_number': next_page_number
    })

@login_required
def manage_leads(request):
    return render(request, 'lead/leads.html')

"""
@login_required
def add_lead(request):
    form=AddLeadForm()
    if request.method == 'POST':
        form=AddLeadForm(request.POST)
        if form.is_valid():
            lead=form.save(commit=False)
            lead.created_by=request.user
            lead.save()
            return redirect('dashboard') 
    
                       
    return render(request, 'lead/manual_lead.html')
"""

@login_required
def manual_lead(request):
    form=AddLeadForm()
    if request.method == 'POST':
        form=AddLeadForm(request.POST)
        if form.is_valid():
            lead=form.save(commit=False)
            lead.created_by=request.user
            lead.save()
            return redirect('dashboard') 
        
                       
    return render(request, 'lead/manual_lead.html',{'form':form})

@login_required
def webscraping(request):
    form=WebScrapingForm()
    
    if request.method == 'POST':
        form=WebScrapingForm(request.POST)
        if form.is_valid():
            webscraping=form.save(commit=False)
            webscraping.submitted_by=request.user
            webscraping.submitted_at=timezone.now()
            webscraping.save()
            
            return redirect('add_lead')
        else:
            print(form.errors)
    return render(request, 'lead/webscraping.html',{'form':form})

