# Generated by Django 4.2 on 2023-04-29 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gridfokuzapp', '0003_addproducts_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addproducts',
            old_name='Profit',
            new_name='Profit_in_precentage',
        ),
        migrations.RenameField(
            model_name='addproducts',
            old_name='Tax',
            new_name='Tax_in_precentage',
        ),
    ]
