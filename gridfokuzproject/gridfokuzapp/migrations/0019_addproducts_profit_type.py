# Generated by Django 4.2 on 2023-07-01 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gridfokuzapp', '0018_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='addproducts',
            name='profit_type',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
