# Generated by Django 4.2 on 2023-05-04 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gridfokuzapp', '0004_rename_profit_addproducts_profit_in_precentage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManualCombo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gridfokuzapp.addproducts')),
            ],
        ),
    ]
