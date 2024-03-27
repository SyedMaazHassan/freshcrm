import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freshcrm.settings')
django.setup()

from django.contrib.auth.models import User


import csv
from  lead.models import Lead

admin_user = User.objects.get(username='admin')
print(admin_user)
def update_leads_from_csv(file_path):
    with open(file_path, 'r',encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            # Assuming the CSV columns are in the same order as the model fields
            company_name, country, city, address, website = row[0], row[1], row[2], row[3], row[4]

            # Create a new lead instance
            lead = Lead.objects.create(
                company_name=company_name,
                country=country,
                city=city,
                address=address,
                website=website,
                created_by=admin_user,
                created_at='2024-01-31 00:00:00',
            )

file_path="./output.csv"
# Call the function with the path to your CSV file
update_leads_from_csv(file_path=file_path)