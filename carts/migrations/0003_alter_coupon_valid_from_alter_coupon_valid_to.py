# Generated by Django 4.0.3 on 2022-04-18 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='valid_from',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='valid_to',
            field=models.DateField(),
        ),
    ]