# Generated by Django 2.0.4 on 2018-04-19 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180419_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nicething',
            name='text',
            field=models.CharField(max_length=400),
        ),
    ]
