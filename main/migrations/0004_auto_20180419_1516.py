# Generated by Django 2.0.4 on 2018-04-19 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_nicething_reported_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nicething',
            name='reported_reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
