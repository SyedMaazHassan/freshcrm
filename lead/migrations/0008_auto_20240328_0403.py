# Generated by Django 3.2.4 on 2024-03-27 23:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lead', '0007_auto_20240328_0359'),
    ]

    operations = [
        migrations.CreateModel(
            name='HKTDCRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('subcategory', models.CharField(max_length=100)),
                ('item', models.CharField(max_length=100)),
                ('source_url', models.CharField(max_length=100)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hktdc_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='webscraping',
            name='source_csv_file',
        ),
        migrations.DeleteModel(
            name='HKTDC',
        ),
    ]
