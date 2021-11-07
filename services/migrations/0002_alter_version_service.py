# Generated by Django 3.2.9 on 2021-11-07 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='service',
            field=models.CharField(choices=[('eks', 'EKS'), ('gke', 'GKE'), ('aks', 'AKS'), ('gcp_cloud_sql', 'Cloud SQL')], max_length=255),
        ),
    ]
