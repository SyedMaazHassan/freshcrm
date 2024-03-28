# Generated by Django 3.2.4 on 2024-03-28 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0009_auto_20240328_0410'),
    ]

    operations = [
        migrations.AddField(
            model_name='hktdcrequest',
            name='status',
            field=models.CharField(default='Failed', max_length=15),
        ),
        migrations.CreateModel(
            name='HKTDCRequestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_file', models.FileField(upload_to='hktdc_results')),
                ('hktdc_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='lead.hktdcrequest')),
            ],
        ),
    ]