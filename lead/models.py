from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from webscrape.hktdc import HKTDC
import json, csv

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
        

def get_choices():
    hktdc = HKTDC()
    item_list = hktdc.get_item_list()
    new_item_list = []
    for i in range(len(item_list)):
        item = item_list[i]
        if item[0] not in new_item_list:
            new_item_list.append(item[0])
    new_item_list = [(item, item) for item in new_item_list]
    return new_item_list

class Webscraping(models.Model):
    CATEGORY_CHOICES = get_choices()
    source_url = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(User, related_name='webscraping',on_delete=models.CASCADE)
    category = models.CharField(max_length=255, null=True, blank=True, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=255, null=True, blank=True)
    item = models.CharField(max_length=255, null=True, blank=True)


class HKTDCRequest(models.Model):
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    source_url = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(User, related_name='hktdc_request',on_delete=models.CASCADE)
    status = models.CharField(max_length = 15, default="Failed")

    def get_csv_data(self):
        return HKTDCRequestResult.objects.filter(hktdc_request = self).first()


    # Assuming `result_instance` is an instance of HKTDCRequestResult
    def read_csv_file(self):
        csv_data_object = self.get_csv_data()

        csv_file = csv_data_object.response_file

        # Ensure the file exists
        if csv_file and hasattr(csv_file, 'path'):
            csv_data = []
            with open(csv_file.path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    csv_data.append(row)
            return csv_data
        else:
            return []


    def scrape_suppliers(self):
        hktdc = HKTDC(hktdc_request_obj=self)
        item_list_data = hktdc.get_item_list_dict()
        items = item_list_data[self.category][self.subcategory]
        focused_item = None
        for item in items:
            if item['item_name'] == self.item:
                focused_item = item

        if not focused_item:
            self.status = "Failed"
            self.save()
            return


        updated_link = focused_item['item_url'].replace("Product-Catalog","Suppliers")            
        hktdc.get_product_suppliers_for_model(
            focused_item['item_name'], 
            updated_link
        )


        self.status = "Success"
        self.save()
        print("Scraping started...")


class HKTDCRequestResult(models.Model):
    response_file = models.FileField(upload_to = 'hktdc_results')
    hktdc_request = models.ForeignKey(HKTDCRequest, on_delete= models.CASCADE, related_name = 'result')