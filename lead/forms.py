from django import forms
from .models import Lead,Webscraping

class AddLeadForm(forms.ModelForm):
    
    class Meta:
        model = Lead
        fields = ('company_name', 'email', 'phone', 'website', 'address', 'city', 'state', 'country', 'zipcode', 'description', 'priority', 'status')
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
            'email': forms.EmailInput(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
            'phone': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
            'website': forms.URLInput(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
            'address': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
            'city': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
            'state': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
            'country': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
            'description': forms.Textarea(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
            'priority': forms.Select(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
            'status': forms.Select(attrs={'class': 'form-input mt-1 block w-full bg-gray-100'}),
        }
        
        
class WebScrapingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WebScrapingForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = True
        self.fields['subcategory'].required = True
        self.fields['item'].required = True

    class Meta:
        model = Webscraping
        fields = ('source_url', 'category', 'subcategory', 'item')
        widgets = {
            'source_url': forms.Select(choices=[('HKTCD.com', 'HKTCD.com')], attrs={'class': 'form-input block w-full bg-gray-100'}),
            'subcategory': forms.Select(choices=[('', '---------')], attrs={'class': 'form-input block w-full bg-gray-100'}),
            'item': forms.Select(choices=[('', '---------')], attrs={'class': 'form-input block w-full bg-gray-100'})
        }


"""
class HKTDCForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        csv_file = "./resouce/product.csv"
        with open('path_to_your_csv_file.csv', newline='') as f:
            reader = csv.reader(f)
            self.fields['main_category'].widget.choices = [(row[0], row[1]) for row in reader]

    class Meta:
        model = Webscraping
        fields = ('source_url', 'main_category', 'sub_category', 'sub_sub_category')
        
        widgets = {
            ''
            
            'main_category': forms.Select(choices=[]),
        }
"""