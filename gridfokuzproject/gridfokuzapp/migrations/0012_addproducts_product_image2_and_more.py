# Generated by Django 4.2 on 2023-06-12 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gridfokuzapp', '0011_addproducts_discription'),
    ]

    operations = [
        migrations.AddField(
            model_name='addproducts',
            name='product_image2',
            field=models.ImageField(null=True, upload_to='product_images'),
        ),
        migrations.AddField(
            model_name='addproducts',
            name='product_image3',
            field=models.ImageField(null=True, upload_to='product_images'),
        ),
    ]
