# Generated by Django 5.1.1 on 2024-09-14 19:48

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce_Website', '0005_alter_produit_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
