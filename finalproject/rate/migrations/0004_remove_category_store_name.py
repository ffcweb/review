# Generated by Django 4.2.7 on 2023-12-19 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0003_category_store_name_alter_store_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='store_name',
        ),
    ]
