from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.manage_leads, name='leads'),    
    path('add_lead/', views.add_lead, name='add_lead'),
    path('webscraping/', views.webscraping, name='webscraping'),
    path('manual_lead/', views.manual_lead, name='manual_lead'),
    path('leads_list/', views.leads_list, name='leads_list'), 
    path('add_lead/', views.add_lead, name='add_lead'),
]
