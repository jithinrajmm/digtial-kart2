# Generated by Django 4.0.3 on 2022-04-19 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('adminpanel', '0002_productoffer_categoryoffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoffer',
            name='category',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='catoffer', to='category.category'),
        ),
    ]