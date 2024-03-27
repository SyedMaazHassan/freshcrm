from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Lead(models.Model):
    LOW='low'
    MEDIUM='medium'
    HIGH='high'
    
    CHOICE_PRIORITY = (
        (LOW,'Low'),
        (MEDIUM,'Medium'),
        (HIGH,'High'),
    )
    
    NEW='new'
    CONTACTED='contacted'
    WON='won'
    LOST='lost'
   
    CHOICE_STATUS = (
        (NEW, 'New'),
        (CONTACTED,'Contacted'),
        (WON,'Won'),
        (LOST,'Lost'),
    )
     
    
    created_by = models.ForeignKey(User, related_name='leads',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    source_url = models.CharField(max_length=100)
    modified_at = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True) 
    phone= models.CharField(max_length=100,blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=100,blank=True, null=True )
    city = models.CharField(max_length=100,blank= True, null=True )
    state = models.CharField(max_length=100,blank=True, null=True )
    country = models.CharField(max_length=100,blank=True, null=True)
    zipcode = models.CharField(max_length=100,blank=True, null=True)
    description = models.CharField(max_length=300,blank=True, null=True)    
    priority = models.CharField(max_length=20,choices=CHOICE_PRIORITY,default=MEDIUM)
    status = models.CharField(max_length=20,choices=CHOICE_STATUS,default=NEW)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.company_name
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Leads"
        verbose_name = "Lead"
        
class Webscraping(models.Model):
    source_url = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(User, related_name='webscraping',on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    

class HKTDC(models.Model):
    main_category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    sub_sub_category = models.CharField(max_length=100)
    source_url = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(User, related_name='hktdc',on_delete=models.CASCADE)
    